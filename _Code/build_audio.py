"""Synthesize per-beat neural voice-over via edge-tts, generate subtle ambient pad,
and export exact frame-aligned timing manifest for the animation renderer.
"""

import asyncio
import json
import os
import subprocess
import wave
from typing import Dict, List

import edge_tts
import numpy as np

from script_data import BEATS

FPS = 30
SAMPLE_RATE = 48000
VOICE = "en-US-AndrewNeural"
RATE = "+6%"  # crisp, engaging teaching pace targeting ~5.25 min total


async def synthesize_beat(text: str, out_mp3: str) -> None:
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
    await communicate.save(out_mp3)


def mp3_to_wav_duration(mp3_path: str, wav_path: str) -> float:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            mp3_path,
            "-ar",
            str(SAMPLE_RATE),
            "-ac",
            "2",
            "-sample_fmt",
            "s16",
            wav_path,
        ],
        check=True,
    )
    with wave.open(wav_path, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
    return frames / float(rate)


def build_ambient_pad(total_sec: float, out_wav: str) -> None:
    """Create a very subtle, warm ambient harmonic pad in Python (no copyright issues)."""
    n_samples = int(round(total_sec * SAMPLE_RATE))
    t = np.linspace(0.0, total_sec, n_samples, endpoint=False, dtype=np.float64)

    # Gentle warm chord progression looping every 32 seconds: C2/G2/D3/E3 -> G -> Am -> F
    chords = [
        [130.81, 196.00, 293.66, 329.63],  # Cadd9
        [123.47, 196.00, 293.66, 392.00],  # G/B
        [110.00, 196.00, 261.63, 329.63],  # Am7
        [87.31, 174.61, 261.63, 329.63],   # Fmaj7
    ]
    chord_len = 8.0
    sig = np.zeros_like(t)

    for i, freqs in enumerate(chords):
        # Smooth periodic envelope for each chord slot in the 32s cycle
        phase = (t - i * chord_len) % (len(chords) * chord_len)
        raw_sin = np.where(phase < chord_len, np.sin(np.pi * phase / chord_len), 0.0)
        env = np.maximum(0.0, raw_sin) ** 1.5
        chord_wave = np.zeros_like(t)
        for idx, f in enumerate(freqs):
            detune = 1.0 + (idx - 1.5) * 0.0008
            chord_wave += 0.25 * np.sin(2.0 * np.pi * f * detune * t)
        sig += env * chord_wave

    # Slow global fade-in / fade-out
    fade = np.ones_like(t)
    fade_samples = min(int(2.5 * SAMPLE_RATE), n_samples // 4)
    fade[:fade_samples] = np.linspace(0.0, 1.0, fade_samples)
    fade[-fade_samples:] = np.linspace(1.0, 0.0, fade_samples)
    sig *= fade

    # Very low level (-28 dB equivalent) so narration is crystal clear
    sig = np.clip(sig * 0.035, -0.95, 0.95)
    pcm = (sig * 32767.0).astype(np.int16)
    stereo = np.column_stack([pcm, pcm]).ravel()

    with wave.open(out_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(stereo.tobytes())


async def main_async() -> None:
    code_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(code_dir, "build_audio")
    os.makedirs(build_dir, exist_ok=True)

    timings: List[Dict] = []
    full_audio_parts: List[np.ndarray] = []
    cursor_sec = 0.0

    for idx, beat in enumerate(BEATS, start=1):
        mp3_path = os.path.join(build_dir, f"{idx:02d}_{beat.beat_id}.mp3")
        wav_path = os.path.join(build_dir, f"{idx:02d}_{beat.beat_id}.wav")
        if not os.path.exists(mp3_path):
            print(f"[{idx}/{len(BEATS)}] Synthesizing {beat.beat_id}...")
            await synthesize_beat(beat.narration, mp3_path)
        else:
            print(f"[{idx}/{len(BEATS)}] Cached {beat.beat_id}")

        speech_dur = mp3_to_wav_duration(mp3_path, wav_path)
        raw_total = speech_dur + beat.post_pause_sec
        n_frames = max(1, int(round(raw_total * FPS)))
        aligned_dur = n_frames / float(FPS)

        with wave.open(wav_path, "rb") as wf:
            pcm = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).reshape(-1, 2)

        target_samples = int(round(aligned_dur * SAMPLE_RATE))
        if len(pcm) < target_samples:
            pad = np.zeros((target_samples - len(pcm), 2), dtype=np.int16)
            beat_pcm = np.vstack([pcm, pad])
        else:
            beat_pcm = pcm[:target_samples]

        full_audio_parts.append(beat_pcm)
        timings.append(
            {
                "index": idx,
                "beat_id": beat.beat_id,
                "scene_num": beat.scene_num,
                "scene_name": beat.scene_name,
                "speech_sec": round(speech_dur, 4),
                "duration_sec": round(aligned_dur, 4),
                "start_sec": round(cursor_sec, 4),
                "end_sec": round(cursor_sec + aligned_dur, 4),
                "frames": n_frames,
            }
        )
        cursor_sec += aligned_dur

    narration_pcm = np.vstack(full_audio_parts)
    narration_wav = os.path.join(build_dir, "narration_full.wav")
    with wave.open(narration_wav, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(narration_pcm.tobytes())

    ambient_wav = os.path.join(build_dir, "ambient_pad.wav")
    build_ambient_pad(cursor_sec, ambient_wav)

    mixed_wav = os.path.join(build_dir, "final_audio.wav")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            narration_wav,
            "-i",
            ambient_wav,
            "-filter_complex",
            "amix=inputs=2:duration=first:weights=1 0.85,aresample=48000",
            "-c:a",
            "pcm_s16le",
            mixed_wav,
        ],
        check=True,
    )

    manifest = {
        "fps": FPS,
        "total_duration_sec": round(cursor_sec, 4),
        "total_frames": sum(t["frames"] for t in timings),
        "voice": VOICE,
        "beats": timings,
    }
    manifest_path = os.path.join(build_dir, "timings.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(
        f"Audio synthesis complete! Total duration: {cursor_sec:.2f}s "
        f"({cursor_sec/60:.2f} min), total frames: {manifest['total_frames']}"
    )


if __name__ == "__main__":
    asyncio.run(main_async())

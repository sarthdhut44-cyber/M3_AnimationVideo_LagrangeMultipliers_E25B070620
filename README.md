# M3 Internal Assessment — Lagrange Multipliers Animation Video

- **Course:** Linear Algebra and Calculus (M3) • Internal Assessment (Project Option 1)
- **Topic:** Lagrange Multipliers (Constrained Optimization)
- **Student Name:** Sarth Onkar Dhut
- **URN / Student ID:** `E25B070620`
- **Batch / Lab Batch:** Turing / Enigma

---

## Learning Objective

> *By the end of this video, the viewer will be able to explain geometrically why constrained extrema occur where the level curves of the objective function are tangent to the constraint curve ($\nabla f = \lambda \nabla g$), and solve a two-variable constrained optimization problem step by step.*

---

## Repository Structure

| Path | Description |
| :--- | :--- |
| [`_Video.mp4`](./_Video.mp4) | Final 1080p 16:9 MP4 animation video (~4 min 45 sec) with clear voice-over narration, subtle ambient chord pad, opening frame, and closing credits/disclosure frame. |
| [`Storyboard.pdf`](./Storyboard.pdf) | 6-scene storyboard detailing visual plans, mathematical content, and narration cues. |
| [`Narration_Script.md`](./Narration_Script.md) | Complete timed narration script broken into 19 synchronized beats across all 6 scenes. |
| [`_Code/`](./_Code/) | Complete runnable Python source code used to verify the math, generate the storyboard PDF, synthesize voice-over audio, and render the 1080p animation. |

### Source Files Inside `_Code/`

- `_Code/script_data.py` — Single source of truth for student metadata, 6-scene plan, and 19 narration beats.
- `_Code/verify_math.py` — Independent numerical & symbolic-style verification of gradients, regularity, extrema, sensitivity ($df^*/dc = \lambda$), and inscribed square area.
- `_Code/generate_storyboard.py` — Generates `Storyboard.pdf` and `Narration_Script.md`.
- `_Code/build_audio.py` — Synthesizes per-beat neural voice-over via `edge-tts`, generates the custom Python ambient pad, and writes `build_audio/timings.json`.
- `_Code/theme.py` — Shared 1080p dark-slate visual palette, easing functions, vector arrow helpers, and contour/circle plotters.
- `_Code/scenes_part1.py` — Animation renderers for Scenes 1–3 (Hook, Concept Introduction, 3D/2D Visual Intuition).
- `_Code/scenes_part2.py` — Animation renderers for Scenes 4–6 (Worked Example, Interpretation, Summary & Credits).
- `_Code/render_video.py` — Multiprocessing 1080p frame renderer piping raw RGB frames to `ffmpeg` and muxing audio into `_Video.mp4`.

---

## Mathematical Verification Summary

**Problem:** Find the global extrema of $f(x, y) = xy$ subject to $g(x, y) = x^2 + y^2 - 8 = 0$.

1. **Gradients & Regularity:**
   $$\nabla f(x, y) = (y, x), \qquad \nabla g(x, y) = (2x, 2y)$$
   $\nabla g = (0, 0)$ only at $(0, 0)$, which violates $0^2 + 0^2 = 8$. Hence $\nabla g \neq \mathbf{0}$ everywhere on the constraint circle.
2. **Lagrange System ($\nabla f = \lambda \nabla g$ and $g = 0$):**
   $$y = 2\lambda x, \qquad x = 2\lambda y, \qquad x^2 + y^2 = 8$$
3. **Zero-Case Check & Solution:**
   If $x = 0$, the system forces $y = 0$, contradicting $x^2 + y^2 = 8$. Thus $x, y \neq 0$, so:
   $$\lambda = \frac{y}{2x} = \frac{x}{2y} \implies y^2 = x^2 \implies y = \pm x$$
   Substituting into $x^2 + y^2 = 8$ gives $2x^2 = 8 \implies x = \pm 2$.
4. **Classification (Extreme Value Theorem on Compact Circle):**
   - **Global Maxima ($f = +4$, $\lambda = +1/2$):** $(2, 2)$ and $(-2, -2)$
   - **Global Minima ($f = -4$, $\lambda = -1/2$):** $(2, -2)$ and $(-2, 2)$
5. **Interpretations:**
   - **Sensitivity:** On $x^2 + y^2 = c$, the optimal value is $f^*(c) = c/2$, so $\frac{df^*}{dc} = \frac{1}{2} = \lambda$.
   - **Inscribed Rectangle:** Maximizing area $4xy$ inside a circle of radius $\sqrt{8}$ yields $x = y = 2$, a $4 \times 4$ square of area $16$.

---

## Reproducing From Source

Requires Python 3.10+ and `ffmpeg`:

```bash
cd _Code
pip install -r requirements.txt
python3 verify_math.py
python3 generate_storyboard.py
python3 build_audio.py
python3 render_video.py
```

---

## Credits & AI Tool Disclosure

- **Mathematical References:**
  - James Stewart, *Multivariable Calculus* — Section on Lagrange Multipliers
  - Gilbert Strang, *Calculus* & MIT OpenCourseWare 18.02 (*Multivariable Calculus*)
- **Audio & Music Credits:**
  - Voice-over narration synthesized with Microsoft Edge Neural TTS (`edge-tts`, voice `en-US-AndrewNeural`).
  - Background harmonic chord pad synthesized directly in Python (`numpy`, original royalty-free waveform mixed at low volume beneath narration).
- **AI Tool Disclosure:**
  - AI assistance was used to structure the 6-scene storyboard, refine narration pacing, write the Python/Matplotlib/FFmpeg animation rendering scripts, and synthesize the voice-over via `edge-tts`. All mathematical derivations, calculations, and code logic were independently verified using `verify_math.py`.

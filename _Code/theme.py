"""Shared visual theme, easing utilities, and Matplotlib drawing helpers for 1080p animation."""

from typing import List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import numpy as np


WIDTH = 1920
HEIGHT = 1080
DPI = 100

# Midnight academic color palette
BG_COLOR = "#0B1120"
PANEL_BG = "#131C31"
PANEL_BORDER = "#2A3B5E"
PANEL_HIGHLIGHT = "#1B2A4A"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"
TEXT_MUTED = "#64748B"

COLOR_CONSTRAINT = "#F8FAFC"  # Crisp white
COLOR_LEVEL = "#38BDF8"       # Sky cyan
COLOR_GRAD_F = "#FB923C"      # Orange-gold
COLOR_GRAD_G = "#A78BFA"      # Bright violet
COLOR_TANGENT = "#FACC15"     # Warm yellow
COLOR_MAX = "#34D399"         # Emerald green
COLOR_MIN = "#F43F5E"         # Rose red
COLOR_ACCENT = "#38BDF8"      # Sky blue


def configure_matplotlib() -> None:
    plt.rcParams.update({
        "figure.facecolor": BG_COLOR,
        "axes.facecolor": BG_COLOR,
        "savefig.facecolor": BG_COLOR,
        "text.color": TEXT_PRIMARY,
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "stix",
        "axes.edgecolor": "#334155",
        "axes.labelcolor": TEXT_SECONDARY,
        "xtick.color": TEXT_MUTED,
        "ytick.color": TEXT_MUTED,
    })


def ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3


def sub_progress(p: float, start: float, end: float, ease: bool = True) -> float:
    if end <= start:
        return 1.0 if p >= start else 0.0
    val = (p - start) / (end - start)
    val = max(0.0, min(1.0, val))
    return ease_in_out(val) if ease else val


def new_canvas() -> Tuple[Figure, plt.Axes]:
    """Create a 1920x1080 figure with a full-bleed normalized [0, 1] x [0, 1] overlay axis."""
    fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI, facecolor=BG_COLOR)
    overlay = fig.add_axes([0.0, 0.0, 1.0, 1.0], facecolor="none")
    overlay.set_xlim(0.0, 1.0)
    overlay.set_ylim(0.0, 1.0)
    overlay.axis("off")
    return fig, overlay


def draw_header_and_progress(
    overlay: plt.Axes,
    scene_num: int,
    scene_label: str,
    global_progress: float,
) -> None:
    """Draw consistent top header bar and subtle bottom scene progress bar."""
    # Top subtle divider
    overlay.plot([0.04, 0.96], [0.915, 0.915], color="#1E293B", lw=1.5, zorder=20)

    # Scene badge
    badge = patches.FancyBboxPatch(
        (0.04, 0.932),
        0.24,
        0.042,
        boxstyle="round,pad=0.004,rounding_size=0.01",
        facecolor=PANEL_HIGHLIGHT,
        edgecolor=COLOR_ACCENT,
        linewidth=1.2,
        zorder=20,
    )
    overlay.add_patch(badge)
    overlay.text(
        0.16,
        0.953,
        scene_label.upper(),
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=COLOR_ACCENT,
        zorder=21,
    )

    overlay.text(
        0.96,
        0.953,
        "M3 • Lagrange Multipliers  |  Sarth Onkar Dhut (E25B070620)",
        ha="right",
        va="center",
        fontsize=12.5,
        color=TEXT_SECONDARY,
        zorder=21,
    )

    # Bottom progress bar
    overlay.plot([0.04, 0.96], [0.025, 0.025], color="#1E293B", lw=4, solid_capstyle="round", zorder=20)
    bar_end = 0.04 + 0.92 * max(0.0, min(1.0, global_progress))
    overlay.plot([0.04, bar_end], [0.025, 0.025], color=COLOR_ACCENT, lw=4, solid_capstyle="round", zorder=21)


def draw_card(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    facecolor: str = PANEL_BG,
    edgecolor: str = PANEL_BORDER,
    lw: float = 1.6,
    alpha: float = 1.0,
    zorder: Optional[int] = None,
) -> patches.FancyBboxPatch:
    if zorder is None:
        zorder = 2 if facecolor == PANEL_HIGHLIGHT else 1
    box = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.016",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        alpha=alpha,
        zorder=zorder,
    )
    ax.add_patch(box)
    return box


def draw_arrow_2d(
    ax: plt.Axes,
    origin: Tuple[float, float],
    vec: Tuple[float, float],
    color: str,
    label: Optional[str] = None,
    label_offset: Tuple[float, float] = (0.15, 0.15),
    lw: float = 3.0,
    alpha: float = 1.0,
    scale: float = 1.0,
    zorder: int = 12,
    fontsize: int = 15,
) -> None:
    vx, vy = vec[0] * scale, vec[1] * scale
    if np.hypot(vx, vy) < 1e-4 or alpha <= 0.01:
        return
    arrow = patches.FancyArrowPatch(
        origin,
        (origin[0] + vx, origin[1] + vy),
        arrowstyle="-|>,head_length=8,head_width=5",
        color=color,
        linewidth=lw,
        alpha=alpha,
        zorder=zorder,
    )
    ax.add_patch(arrow)
    if label:
        ax.text(
            origin[0] + vx + label_offset[0],
            origin[1] + vy + label_offset[1],
            label,
            color=color,
            fontsize=fontsize,
            fontweight="bold",
            ha="center",
            va="center",
            alpha=alpha,
            zorder=zorder + 1,
            bbox=dict(boxstyle="round,pad=0.18", facecolor=BG_COLOR, edgecolor="none", alpha=0.75 * alpha),
        )


def setup_2d_math_axes(ax: plt.Axes, lim: float = 4.2) -> None:
    ax.set_facecolor("#0E172A")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axhline(0, color="#334155", lw=1.2, zorder=1)
    ax.axvline(0, color="#334155", lw=1.2, zorder=1)
    ax.grid(True, color="#1E293B", linestyle="-", linewidth=0.8, alpha=0.7, zorder=0)
    ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax.set_yticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax.tick_params(labelsize=11, colors=TEXT_SECONDARY)
    ax.set_xlabel(r"$x$", fontsize=15, color=TEXT_PRIMARY, labelpad=4)
    ax.set_ylabel(r"$y$", fontsize=15, color=TEXT_PRIMARY, labelpad=4)
    for spine in ax.spines.values():
        spine.set_color("#334155")
        spine.set_linewidth(1.2)


def draw_hyperbolas(
    ax: plt.Axes,
    levels: List[float],
    highlight_k: Optional[float] = None,
    alpha: float = 0.55,
) -> None:
    x_pos = np.linspace(0.18, 4.2, 260)
    x_neg = np.linspace(-4.2, -0.18, 260)
    for k in levels:
        is_hi = highlight_k is not None and abs(k - highlight_k) < 1e-3
        col = COLOR_TANGENT if is_hi else COLOR_LEVEL
        lw = 2.8 if is_hi else 1.35
        a = min(1.0, alpha * (1.7 if is_hi else 0.75))
        ls = "-" if k >= 0 else "--"
        if abs(k) < 1e-6:
            ax.axhline(0, color=col, lw=lw, alpha=a * 0.6, ls=":", zorder=2)
            ax.axvline(0, color=col, lw=lw, alpha=a * 0.6, ls=":", zorder=2)
            continue
        y_pos = k / x_pos
        y_neg = k / x_neg
        mask_p = np.abs(y_pos) <= 4.2
        mask_n = np.abs(y_neg) <= 4.2
        ax.plot(x_pos[mask_p], y_pos[mask_p], color=col, lw=lw, alpha=a, ls=ls, zorder=3 if is_hi else 2)
        ax.plot(x_neg[mask_n], y_neg[mask_n], color=col, lw=lw, alpha=a, ls=ls, zorder=3 if is_hi else 2)


def draw_constraint_circle(ax: plt.Axes, radius: float = np.sqrt(8.0), lw: float = 3.0, alpha: float = 1.0) -> None:
    th = np.linspace(0, 2 * np.pi, 360)
    ax.plot(radius * np.cos(th), radius * np.sin(th), color=COLOR_CONSTRAINT, lw=lw, alpha=alpha, zorder=5)


def figure_to_rgb_bytes(fig: Figure) -> bytes:
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    # Drop alpha channel cleanly for rgb24 ffmpeg pipe
    return buf[:, :, :3].tobytes()

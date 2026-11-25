"""Animation renderers for Scenes 4, 5, and 6."""

import matplotlib.patches as patches
import numpy as np

from script_data import BATCH, CONCEPT, COURSE, LAB_BATCH, STUDENT_NAME, STUDENT_URN
from theme import (
    BG_COLOR,
    COLOR_ACCENT,
    COLOR_CONSTRAINT,
    COLOR_GRAD_F,
    COLOR_GRAD_G,
    COLOR_LEVEL,
    COLOR_MAX,
    COLOR_MIN,
    COLOR_TANGENT,
    PANEL_BG,
    PANEL_BORDER,
    PANEL_HIGHLIGHT,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    draw_arrow_2d,
    draw_card,
    draw_constraint_circle,
    draw_header_and_progress,
    draw_hyperbolas,
    new_canvas,
    setup_2d_math_axes,
    sub_progress,
)


def _draw_worked_example_left_base(fig, highlight_origin: bool = False):
    ax = fig.add_axes([0.04, 0.11, 0.43, 0.76])
    setup_2d_math_axes(ax, lim=3.8)
    draw_hyperbolas(ax, [-4, -2, 2, 4], alpha=0.40)
    draw_constraint_circle(ax, radius=np.sqrt(8.0), lw=3.0)
    if highlight_origin:
        ax.scatter([0], [0], color=COLOR_MIN, s=110, marker="x", lw=2.8, zorder=10)
        ax.text(0.16, -0.34, r"$(0,0) \notin$ circle", color=COLOR_MIN, fontsize=11.5, fontweight="bold")
    return ax


def render_s4_setup(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 4, "Scene 4 • Worked Example", gp)

    ax = _draw_worked_example_left_base(fig, highlight_origin=(p > 0.50))
    ax.set_title(r"Optimize $f(x, y) = xy$ on $x^2 + y^2 = 8$", fontsize=16.5, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.50, 0.11, 0.46, 0.76)
    ov.text(0.73, 0.82, "Step 1: Gradients & Regularity", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_ACCENT)

    a1 = sub_progress(p, 0.02, 0.28)
    a2 = sub_progress(p, 0.28, 0.58)
    a3 = sub_progress(p, 0.58, 0.88)

    ov.text(0.53, 0.72,
            r"Objective:  $f(x, y) = xy$" + "\n" +
            r"Constraint:  $g(x, y) = x^2 + y^2 - 8 = 0$",
            ha="left", va="center", fontsize=16, color=TEXT_PRIMARY, linespacing=1.55, alpha=a1)

    ov.text(0.53, 0.54,
            r"$\nabla f(x, y) = \left(\frac{\partial f}{\partial x},\, \frac{\partial f}{\partial y}\right) = (y,\, x)$" + "\n\n" +
            r"$\nabla g(x, y) = \left(\frac{\partial g}{\partial x},\, \frac{\partial g}{\partial y}\right) = (2x,\, 2y)$",
            ha="left", va="center", fontsize=16, color=COLOR_GRAD_F, linespacing=1.35, alpha=a2)

    draw_card(ov, 0.525, 0.16, 0.41, 0.22, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MAX, lw=1.6, alpha=a3)
    ov.text(0.73, 0.32, "Regularity Check", ha="center", va="center",
            fontsize=16.5, fontweight="bold", color=COLOR_MAX, alpha=a3)
    ov.text(0.73, 0.23,
            r"$\nabla g = (0,0) \Longleftrightarrow (x,y) = (0,0)$" + "\n" +
            r"Since $0^2 + 0^2 \neq 8$, $\nabla g \neq \mathbf{0}$ everywhere on the circle!",
            ha="center", va="center", fontsize=14, color=TEXT_PRIMARY, linespacing=1.45, alpha=a3)
    return fig


def render_s4_system(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 4, "Scene 4 • Worked Example", gp)

    ax = _draw_worked_example_left_base(fig)
    th = np.deg2rad(45.0)
    r = np.sqrt(8.0)
    px, py = r * np.cos(th), r * np.sin(th)
    ax.scatter([px], [py], color=COLOR_TANGENT, s=110, zorder=10)
    draw_arrow_2d(ax, (px, py), (0.85, 0.85), COLOR_GRAD_F, r"$\nabla f$", (-0.25, 0.22), lw=3.0)
    draw_arrow_2d(ax, (px, py), (1.30, 1.30), COLOR_GRAD_G, r"$\lambda \nabla g$", (0.35, -0.15), lw=2.4)
    ax.set_title(r"Lagrange System: $\nabla f = \lambda\,\nabla g$", fontsize=16.5, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.50, 0.11, 0.46, 0.76)
    ov.text(0.73, 0.82, "Step 2: Set Up the System", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_ACCENT)

    a1 = sub_progress(p, 0.05, 0.30)
    a2 = sub_progress(p, 0.28, 0.55)
    a3 = sub_progress(p, 0.52, 0.80)

    ov.text(0.73, 0.71, r"$(y,\; x) = \lambda\,(2x,\; 2y)$",
            ha="center", va="center", fontsize=21, fontweight="bold", color=COLOR_TANGENT, alpha=a1)

    draw_card(ov, 0.54, 0.24, 0.38, 0.38, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_ACCENT, lw=1.8, alpha=a2)
    ov.text(0.58, 0.54, r"$(1)\quad y = 2\lambda x$", ha="left", va="center", fontsize=20, color=TEXT_PRIMARY, alpha=a2)
    ov.text(0.58, 0.43, r"$(2)\quad x = 2\lambda y$", ha="left", va="center", fontsize=20, color=TEXT_PRIMARY, alpha=a2)
    ov.text(0.58, 0.32, r"$(3)\quad x^2 + y^2 = 8$", ha="left", va="center", fontsize=20, color=COLOR_CONSTRAINT, alpha=a3)
    return fig


def render_s4_solve(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 4, "Scene 4 • Worked Example", gp)

    ax = _draw_worked_example_left_base(fig)
    a_lines = sub_progress(p, 0.55, 0.90)
    if a_lines > 0.02:
        t = np.linspace(-3.4, 3.4, 100)
        ax.plot(t, t, color=COLOR_MAX, ls="--", lw=2.4, alpha=a_lines, zorder=7, label=r"$y = x$")
        ax.plot(t, -t, color=COLOR_MIN, ls="--", lw=2.4, alpha=a_lines, zorder=7, label=r"$y = -x$")
        ax.text(2.7, 3.15, r"$y = x$", color=COLOR_MAX, fontsize=13, fontweight="bold", alpha=a_lines)
        ax.text(2.6, -3.25, r"$y = -x$", color=COLOR_MIN, fontsize=13, fontweight="bold", alpha=a_lines)
    ax.set_title("Solving Without Dividing by Zero", fontsize=16.5, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.50, 0.11, 0.46, 0.76)
    ov.text(0.73, 0.82, "Step 3: Solve Carefully", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_ACCENT)

    a1 = sub_progress(p, 0.02, 0.35)
    a2 = sub_progress(p, 0.32, 0.65)
    a3 = sub_progress(p, 0.62, 0.90)

    draw_card(ov, 0.525, 0.57, 0.41, 0.18, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_TANGENT, lw=1.5, alpha=a1)
    ov.text(0.73, 0.70, "Zero-Case Check", ha="center", va="center",
            fontsize=15.5, fontweight="bold", color=COLOR_TANGENT, alpha=a1)
    ov.text(0.73, 0.62,
            r"If $x = 0$, Eq. (1) $\Rightarrow y = 0$, violating $x^2+y^2=8$." + "\n" +
            r"Hence $x \neq 0$ and $y \neq 0$ (safe to divide!).",
            ha="center", va="center", fontsize=14, color=TEXT_PRIMARY, linespacing=1.4, alpha=a1)

    ov.text(0.54, 0.44,
            r"Isolate $\lambda$:   $\frac{y}{2x} = \lambda = \frac{x}{2y}$",
            ha="left", va="center", fontsize=18.5, color=TEXT_PRIMARY, alpha=a2)

    ov.text(0.54, 0.31,
            r"Cross-multiply:   $y^2 = x^2$",
            ha="left", va="center", fontsize=18.5, color=COLOR_ACCENT, alpha=a3)

    draw_card(ov, 0.58, 0.15, 0.30, 0.10, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MAX, lw=1.8, alpha=a3)
    ov.text(0.73, 0.20, r"$y = \pm x$", ha="center", va="center",
            fontsize=22, fontweight="bold", color=COLOR_MAX, alpha=a3)
    return fig


def render_s4_candidates(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 4, "Scene 4 • Worked Example", gp)

    ax = _draw_worked_example_left_base(fig)
    t = np.linspace(-3.4, 3.4, 100)
    ax.plot(t, t, color=COLOR_MAX, ls="--", lw=1.8, alpha=0.55)
    ax.plot(t, -t, color=COLOR_MIN, ls="--", lw=1.8, alpha=0.55)

    pts = [
        (2, 2, COLOR_MAX, (0.28, 0.28), "(2, 2)"),
        (-2, -2, COLOR_MAX, (-0.45, -0.38), "(-2, -2)"),
        (2, -2, COLOR_MIN, (0.35, -0.35), "(2, -2)"),
        (-2, 2, COLOR_MIN, (-0.48, 0.28), "(-2, 2)"),
    ]
    for i, (px, py, col, off, lbl) in enumerate(pts):
        ap = sub_progress(p, 0.28 + 0.12 * i, 0.44 + 0.12 * i)
        if ap > 0.02:
            ax.scatter([px], [py], color=col, s=150 * ap, edgecolor="#FFFFFF", lw=1.8, zorder=10, alpha=ap)
            ax.text(px + off[0], py + off[1], lbl, color=col, fontsize=13, fontweight="bold", alpha=ap)

    ax.set_title("4 Candidate Points on Compact Circle", fontsize=16.5, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.50, 0.11, 0.46, 0.76)
    ov.text(0.73, 0.82, "Step 4: Find Candidate Points", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_ACCENT)

    a1 = sub_progress(p, 0.02, 0.30)
    a2 = sub_progress(p, 0.30, 0.60)
    a3 = sub_progress(p, 0.62, 0.90)

    ov.text(0.54, 0.68,
            r"Substitute $y^2 = x^2$ into $x^2 + y^2 = 8$:" + "\n" +
            r"$2x^2 = 8 \;\Longrightarrow\; x^2 = 4 \;\Longrightarrow\; x = \pm 2$",
            ha="left", va="center", fontsize=16.5, color=TEXT_PRIMARY, linespacing=1.55, alpha=a1)

    ov.text(0.54, 0.49,
            "Candidates:\n"
            r"• $(2, 2),\; (-2, -2)$   [from $y = x$]" + "\n"
            r"• $(2, -2),\; (-2, 2)$   [from $y = -x$]",
            ha="left", va="center", fontsize=16, color=COLOR_TANGENT, linespacing=1.55, alpha=a2)

    draw_card(ov, 0.525, 0.16, 0.41, 0.19, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_ACCENT, lw=1.6, alpha=a3)
    ov.text(0.73, 0.295, "Extreme Value Theorem", ha="center", va="center",
            fontsize=16, fontweight="bold", color=COLOR_ACCENT, alpha=a3)
    ov.text(0.73, 0.215,
            "Circle is closed & bounded (compact) and f is continuous,\n"
            "so global max & min are guaranteed among these 4 points.",
            ha="center", va="center", fontsize=13.5, color=TEXT_PRIMARY, linespacing=1.4, alpha=a3)
    return fig


def render_s4_evaluate(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 4, "Scene 4 • Worked Example", gp)

    ax = fig.add_axes([0.04, 0.11, 0.43, 0.76])
    setup_2d_math_axes(ax, lim=3.8)
    draw_hyperbolas(ax, [-4, 4], alpha=0.85)
    # Color-highlight xy=4 in emerald and xy=-4 in rose
    xp = np.linspace(1.05, 3.7, 200)
    ax.plot(xp, 4.0 / xp, color=COLOR_MAX, lw=2.6, zorder=4)
    ax.plot(-xp, -4.0 / xp, color=COLOR_MAX, lw=2.6, zorder=4)
    ax.plot(xp, -4.0 / xp, color=COLOR_MIN, lw=2.6, ls="--", zorder=4)
    ax.plot(-xp, 4.0 / xp, color=COLOR_MIN, lw=2.6, ls="--", zorder=4)
    draw_constraint_circle(ax, radius=np.sqrt(8.0), lw=3.0)

    ax.scatter([2, -2], [2, -2], color=COLOR_MAX, s=150, edgecolor="#FFFFFF", lw=1.8, zorder=10)
    ax.scatter([2, -2], [-2, 2], color=COLOR_MIN, s=150, edgecolor="#FFFFFF", lw=1.8, zorder=10)
    ax.text(2.22, 2.22, "Max +4", color=COLOR_MAX, fontsize=12.5, fontweight="bold")
    ax.text(-3.25, -2.45, "Max +4", color=COLOR_MAX, fontsize=12.5, fontweight="bold")
    ax.text(2.22, -2.35, "Min -4", color=COLOR_MIN, fontsize=12.5, fontweight="bold")
    ax.text(-3.25, 2.22, "Min -4", color=COLOR_MIN, fontsize=12.5, fontweight="bold")
    ax.set_title("Evaluating All 4 Critical Points", fontsize=16.5, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.50, 0.11, 0.46, 0.76)
    ov.text(0.73, 0.82, "Step 5: Evaluate & Classify", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_ACCENT)

    rows = [
        (0.64, "(2, 2)", "f = +4", r"$\lambda = +1/2$", "Global Max", COLOR_MAX, sub_progress(p, 0.05, 0.30)),
        (0.51, "(-2, -2)", "f = +4", r"$\lambda = +1/2$", "Global Max", COLOR_MAX, sub_progress(p, 0.22, 0.48)),
        (0.36, "(2, -2)", "f = -4", r"$\lambda = -1/2$", "Global Min", COLOR_MIN, sub_progress(p, 0.45, 0.72)),
        (0.23, "(-2, 2)", "f = -4", r"$\lambda = -1/2$", "Global Min", COLOR_MIN, sub_progress(p, 0.65, 0.90)),
    ]
    for ry, pt, fval, lam, cls, col, a in rows:
        draw_card(ov, 0.53, ry - 0.045, 0.40, 0.095, facecolor=PANEL_HIGHLIGHT, edgecolor=col, lw=1.6, alpha=a)
        ov.text(0.555, ry, pt, ha="left", va="center", fontsize=15.5, fontweight="bold", color=TEXT_PRIMARY, alpha=a)
        ov.text(0.655, ry, fval, ha="left", va="center", fontsize=15.5, fontweight="bold", color=col, alpha=a)
        ov.text(0.755, ry, lam, ha="left", va="center", fontsize=15, color=TEXT_SECONDARY, alpha=a)
        ov.text(0.915, ry, cls, ha="right", va="center", fontsize=14.5, fontweight="bold", color=col, alpha=a)
    return fig


def render_s5_geometry(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 5, "Scene 5 • Interpretation", gp)

    ax = fig.add_axes([0.04, 0.11, 0.46, 0.76])
    setup_2d_math_axes(ax, lim=4.1)
    draw_hyperbolas(ax, [-4, -2, 2, 4], alpha=0.35)
    draw_constraint_circle(ax, radius=np.sqrt(8.0), lw=3.0)

    a_max = sub_progress(p, 0.05, 0.45)
    a_min = sub_progress(p, 0.45, 0.85)

    # Maxima: same direction outward
    for sx, sy in [(2, 2), (-2, -2)]:
        ax.scatter([sx], [sy], color=COLOR_MAX, s=140, zorder=10, alpha=a_max)
        u = np.array([sx, sy], dtype=float) / np.sqrt(8.0)
        draw_arrow_2d(ax, (sx, sy), tuple(1.35 * u), COLOR_GRAD_G, r"$\nabla g$", (0.28 * np.sign(sx), -0.10), lw=2.6, alpha=a_max, fontsize=12)
        draw_arrow_2d(ax, (sx, sy), tuple(0.85 * u), COLOR_GRAD_F, r"$\nabla f$", (-0.25 * np.sign(sx), 0.25 * np.sign(sy)), lw=3.4, alpha=a_max, fontsize=12)

    # Minima: opposite direction
    for sx, sy in [(2, -2), (-2, 2)]:
        ax.scatter([sx], [sy], color=COLOR_MIN, s=140, zorder=10, alpha=a_min)
        ug = np.array([sx, sy], dtype=float) / np.sqrt(8.0)
        uf = np.array([sy, sx], dtype=float) / np.sqrt(8.0)  # exactly -ug!
        draw_arrow_2d(ax, (sx, sy), tuple(1.25 * ug), COLOR_GRAD_G, r"$\nabla g$", (0.20 * np.sign(sx), 0.18 * np.sign(sy)), lw=2.6, alpha=a_min, fontsize=12)
        draw_arrow_2d(ax, (sx, sy), tuple(1.05 * uf), COLOR_GRAD_F, r"$\nabla f$", (-0.22 * np.sign(sx), -0.22 * np.sign(sy)), lw=3.4, alpha=a_min, fontsize=12)

    ax.set_title(r"Sign of $\lambda$ = Relative Orientation of Gradients", fontsize=16, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.53, 0.14, 0.43, 0.72)
    ov.text(0.745, 0.79, "Geometric Meaning of Sign(λ)", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_ACCENT)

    draw_card(ov, 0.555, 0.48, 0.38, 0.23, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MAX, lw=1.8, alpha=a_max)
    ov.text(0.745, 0.65, r"At Maxima: $\lambda = +\frac{1}{2} > 0$", ha="center", va="center",
            fontsize=17, fontweight="bold", color=COLOR_MAX, alpha=a_max)
    ov.text(0.745, 0.55,
            r"$\nabla f$ and $\nabla g$ point in the SAME direction." + "\n"
            "Expanding the circle increases f!",
            ha="center", va="center", fontsize=14.5, color=TEXT_PRIMARY, linespacing=1.4, alpha=a_max)

    draw_card(ov, 0.555, 0.20, 0.38, 0.23, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MIN, lw=1.8, alpha=a_min)
    ov.text(0.745, 0.37, r"At Minima: $\lambda = -\frac{1}{2} < 0$", ha="center", va="center",
            fontsize=17, fontweight="bold", color=COLOR_MIN, alpha=a_min)
    ov.text(0.745, 0.27,
            r"$\nabla f$ and $\nabla g$ point in OPPOSITE directions." + "\n"
            "Expanding the circle lowers f even further!",
            ha="center", va="center", fontsize=14.5, color=TEXT_PRIMARY, linespacing=1.4, alpha=a_min)
    return fig


def render_s5_lambda_meaning(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 5, "Scene 5 • Interpretation", gp)

    ax = fig.add_axes([0.04, 0.11, 0.45, 0.76])
    setup_2d_math_axes(ax, lim=4.0)

    # First half: animate radius c from 4 -> 12 -> 8; second half: highlight 4x4 inscribed square
    if p < 0.55:
        c_val = 4.0 + 8.0 * sub_progress(p, 0.05, 0.50)
    else:
        c_val = 12.0 - 4.0 * sub_progress(p, 0.55, 0.75)
    r_val = np.sqrt(c_val)
    opt_xy = np.sqrt(c_val / 2.0)
    f_star = c_val / 2.0

    draw_hyperbolas(ax, [2, 4, 6], highlight_k=f_star, alpha=0.50)
    draw_constraint_circle(ax, radius=r_val, lw=3.0)

    # Inscribed square preview growing in second half
    a_sq = sub_progress(p, 0.58, 0.88)
    if a_sq > 0.02:
        rect = patches.Rectangle((-2, -2), 4, 4, facecolor=COLOR_MAX, alpha=0.22 * a_sq,
                                 edgecolor=COLOR_MAX, lw=2.8, zorder=6)
        ax.add_patch(rect)
        ax.text(0, 0, "4 × 4 Square\nArea = 16", ha="center", va="center",
                color=COLOR_MAX, fontsize=14, fontweight="bold", alpha=a_sq,
                bbox=dict(boxstyle="round,pad=0.25", facecolor=BG_COLOR, edgecolor=COLOR_MAX, alpha=0.85 * a_sq))

    ax.scatter([opt_xy], [opt_xy], color=COLOR_MAX, s=130, zorder=10)
    ax.set_title(rf"Relaxing Budget: $c = {c_val:.1f} \;\Rightarrow\; f^* = {f_star:.2f}$",
                 fontsize=16, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.52, 0.14, 0.44, 0.72)
    ov.text(0.74, 0.79, "Two Real-World Interpretations", ha="center", va="center",
            fontsize=20, fontweight="bold", color=COLOR_ACCENT)

    a1 = sub_progress(p, 0.05, 0.40)
    a2 = sub_progress(p, 0.55, 0.85)

    draw_card(ov, 0.545, 0.47, 0.39, 0.25, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_TANGENT, lw=1.8, alpha=a1)
    ov.text(0.74, 0.67, "1. Sensitivity (Shadow Price)", ha="center", va="center",
            fontsize=17, fontweight="bold", color=COLOR_TANGENT, alpha=a1)
    ov.text(0.74, 0.555,
            r"For $x^2 + y^2 = c$,  $f^*(c) = \frac{c}{2}$." + "\n" +
            r"$\frac{df^*}{dc} = \frac{1}{2} = \lambda$  (rate of optimum gain per unit $c$)",
            ha="center", va="center", fontsize=14.5, color=TEXT_PRIMARY, linespacing=1.45, alpha=a1)

    draw_card(ov, 0.545, 0.19, 0.39, 0.23, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MAX, lw=1.8, alpha=a2)
    ov.text(0.74, 0.37, "2. Inscribed Rectangle Solved!", ha="center", va="center",
            fontsize=17, fontweight="bold", color=COLOR_MAX, alpha=a2)
    ov.text(0.74, 0.265,
            "Optimal corner $(2, 2)$ gives width $2x=4$, height $2y=4$.\n"
            "The largest inscribed rectangle is a 4 × 4 square (Area = 16).",
            ha="center", va="center", fontsize=14, color=TEXT_PRIMARY, linespacing=1.45, alpha=a2)
    return fig


def render_s6_summary(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 6, "Scene 6 • Summary & Credits", gp)

    ov.text(0.50, 0.84, "3 Core Takeaways", ha="center", va="center",
            fontsize=28, fontweight="bold", color=TEXT_PRIMARY)

    cards = [
        (0.06, sub_progress(p, 0.02, 0.30), COLOR_ACCENT, "1. Tangency = Parallel Gradients",
         r"Constrained extrema occur where level curves of $f$ kiss $g = c$, making $\nabla f \cdot \mathbf{T} = 0$ and $\nabla f = \lambda\,\nabla g$."),
        (0.36, sub_progress(p, 0.28, 0.60), COLOR_TANGENT, "2. Rigor & Edge Cases",
         r"Always verify regularity ($\nabla g \neq \mathbf{0}$ on the constraint) and check zero cases before dividing by variables."),
        (0.66, sub_progress(p, 0.58, 0.88), COLOR_MAX, "3. What λ Tells You",
         r"The sign of $\lambda$ reveals alignment ($\pm$), and its magnitude measures constraint sensitivity $\lambda = \frac{df^*}{dc}$."),
    ]
    for idx, (x0, a, col, title, body) in enumerate(cards):
        draw_card(ov, x0, 0.20, 0.28, 0.54, facecolor=PANEL_BG, edgecolor=col, lw=2.2, alpha=a)
        ov.text(x0 + 0.14, 0.65, title, ha="center", va="center",
                fontsize=17.5, fontweight="bold", color=col, alpha=a)
        ov.plot([x0 + 0.03, x0 + 0.25], [0.59, 0.59], color=PANEL_BORDER, lw=1.4, alpha=a, zorder=4)
        # Wrap text manually for crisp layout
        if idx == 0:
            txt = (
                "Constrained extrema occur\nwhere level curves of f kiss\n"
                "the constraint g = c.\n\n"
                r"$\nabla f \cdot \mathbf{T} = 0 \;\Longrightarrow\; \nabla f = \lambda\,\nabla g$"
            )
        elif idx == 1:
            txt = (
                "Always verify regularity\n"
                r"($\nabla g \neq \mathbf{0}$ on constraint)" + "\n"
                "and check zero cases\n"
                "before dividing variables."
            )
        else:
            txt = (
                "The sign of λ shows\n"
                "gradient orientation (±),\n"
                "and its value equals\n"
                r"sensitivity: $\lambda = \frac{df^*}{dc}$."
            )
        ov.text(x0 + 0.14, 0.39, txt, ha="center", va="center",
                fontsize=15.5, color=TEXT_PRIMARY, linespacing=1.55, alpha=a)
    return fig


def render_s6_credits(p: float, gp: float):
    fig, ov = new_canvas()
    a = sub_progress(p, 0.0, 0.25)

    draw_card(ov, 0.08, 0.10, 0.84, 0.80, facecolor=PANEL_BG, edgecolor=COLOR_ACCENT, lw=2.0, alpha=a)
    ov.text(0.50, 0.82, "Thank You for Watching", ha="center", va="center",
            fontsize=30, fontweight="bold", color=TEXT_PRIMARY, alpha=a)
    ov.text(0.50, 0.755,
            f"{STUDENT_NAME}   |   URN: {STUDENT_URN}   |   Batch: {BATCH}   |   Lab Batch: {LAB_BATCH}",
            ha="center", va="center", fontsize=15.5, color=COLOR_ACCENT, fontweight="bold", alpha=a)
    ov.plot([0.16, 0.84], [0.71, 0.71], color=PANEL_BORDER, lw=1.5, alpha=a, zorder=4)

    # Left column: References & Audio Credit
    ov.text(0.12, 0.64, "Mathematical References", ha="left", va="center",
            fontsize=17, fontweight="bold", color=COLOR_TANGENT, alpha=a)
    ov.text(0.12, 0.55,
            "• J. Stewart, Multivariable Calculus (Lagrange Multipliers)\n"
            "• G. Strang, Calculus & MIT OCW 18.02 Multivariable Calculus\n"
            "• Extreme Value Theorem on Compact Sets",
            ha="left", va="center", fontsize=13.5, color=TEXT_PRIMARY, linespacing=1.55, alpha=a)

    ov.text(0.12, 0.40, "Audio & Music Credits", ha="left", va="center",
            fontsize=17, fontweight="bold", color=COLOR_MAX, alpha=a)
    ov.text(0.12, 0.31,
            "• Voice-over: Neural TTS (edge-tts, en-US-AndrewNeural)\n"
            "• Background Track: Custom Python-synthesized ambient\n"
            "  harmonic chord pad (original, royalty-free)",
            ha="left", va="center", fontsize=13.5, color=TEXT_PRIMARY, linespacing=1.55, alpha=a)

    # Right column: AI Tool Disclosure & Code Repo
    ov.text(0.53, 0.64, "AI Tool Disclosure (Required)", ha="left", va="center",
            fontsize=17, fontweight="bold", color=COLOR_GRAD_F, alpha=a)
    ov.text(0.53, 0.52,
            "• Scripting & Structure: AI assistance used to organize\n"
            "  the 6-scene storyboard and narration pacing.\n"
            "• Animation Code: Programmatically rendered in Python\n"
            "  (Matplotlib, NumPy, SciPy, Pillow, FFmpeg).\n"
            "• Voice-over: Synthesized via Microsoft Edge TTS.",
            ha="left", va="center", fontsize=13.5, color=TEXT_PRIMARY, linespacing=1.5, alpha=a)

    ov.text(0.53, 0.34, "Source Code & Verification", ha="left", va="center",
            fontsize=17, fontweight="bold", color=COLOR_LEVEL, alpha=a)
    ov.text(0.53, 0.25,
            "• All .py scripts, Storyboard.pdf, and math checks\n"
            "  are available in the public GitHub repository:\n"
            f"  M3_AnimationVideo_LagrangeMultipliers_{STUDENT_URN}",
            ha="left", va="center", fontsize=13.5, color=TEXT_PRIMARY, linespacing=1.5, alpha=a)
    return fig

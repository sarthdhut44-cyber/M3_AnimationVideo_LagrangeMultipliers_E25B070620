"""Animation renderers for Scenes 1, 2, and 3."""

import matplotlib.patches as patches
import numpy as np

from script_data import BATCH, CONCEPT, COURSE, LAB_BATCH, LEARNING_OBJECTIVE, STUDENT_NAME, STUDENT_URN, VIDEO_TITLE
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


def render_s1_title(p: float, gp: float):
    fig, ov = new_canvas()

    # Subtle background math motif (circle + hyperbolas)
    ax = fig.add_axes([0.05, 0.05, 0.90, 0.90], facecolor="none")
    ax.set_xlim(-5.5, 5.5)
    ax.set_ylim(-3.1, 3.1)
    ax.axis("off")
    x = np.linspace(0.2, 5.4, 240)
    for k in [0.5, 1.5, 2.5, 4.0]:
        y = k / x
        m = y <= 3.0
        ax.plot(x[m], y[m], color=COLOR_LEVEL, alpha=0.11, lw=1.6)
        ax.plot(-x[m], -y[m], color=COLOR_LEVEL, alpha=0.11, lw=1.6)
    th = np.linspace(0, 2 * np.pi, 360)
    ax.plot(np.sqrt(8) * np.cos(th), np.sqrt(8) * np.sin(th), color="#FFFFFF", alpha=0.14, lw=2.2)

    a1 = sub_progress(p, 0.0, 0.25)
    a2 = sub_progress(p, 0.12, 0.45)
    a3 = sub_progress(p, 0.30, 0.65)

    draw_card(ov, 0.10, 0.18, 0.80, 0.64, facecolor=PANEL_BG, edgecolor=COLOR_ACCENT, lw=2.0, alpha=0.94 * a1)

    ov.text(
        0.50, 0.72, COURSE.upper(),
        ha="center", va="center", fontsize=15, fontweight="bold", color=COLOR_ACCENT, alpha=a1
    )
    ov.text(
        0.50, 0.59, "Lagrange Multipliers",
        ha="center", va="center", fontsize=46, fontweight="bold", color=TEXT_PRIMARY, alpha=a2
    )
    ov.text(
        0.50, 0.49, "Why Parallel Gradients Solve Constrained Optimization",
        ha="center", va="center", fontsize=23, color="#CBD5E1", alpha=a2
    )

    ov.plot([0.24, 0.76], [0.41, 0.41], color=PANEL_BORDER, lw=1.5, alpha=a3, zorder=4)

    ov.text(
        0.50, 0.33, f"Concept: {CONCEPT}",
        ha="center", va="center", fontsize=17, color=COLOR_TANGENT, fontweight="bold", alpha=a3
    )
    ov.text(
        0.50, 0.255, f"Student: {STUDENT_NAME}   |   URN: {STUDENT_URN}   |   Batch: {BATCH}   |   Lab: {LAB_BATCH}",
        ha="center", va="center", fontsize=16, color=TEXT_PRIMARY, alpha=a3
    )
    return fig


def render_s1_unconstrained(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 1, "Scene 1 • Hook / Context", gp)

    # 3D Saddle surface on left
    ax3d = fig.add_axes([0.04, 0.06, 0.54, 0.77], projection="3d", facecolor=BG_COLOR)
    u = np.linspace(-3.4, 3.4, 48)
    X, Y = np.meshgrid(u, u)
    Z = X * Y
    ax3d.plot_surface(X, Y, Z, cmap="coolwarm", alpha=0.82, edgecolor="#1E293B", linewidth=0.25, antialiased=True)
    ax3d.scatter([0], [0], [0], color=COLOR_TANGENT, s=90, zorder=10)
    ax3d.text(0.2, 0.2, 1.4, "Origin (0, 0, 0)\nSaddle Point", color=COLOR_TANGENT, fontsize=11, fontweight="bold")

    ax3d.set_xlim(-3.5, 3.5)
    ax3d.set_ylim(-3.5, 3.5)
    ax3d.set_zlim(-11, 11)
    ax3d.set_xlabel("x", labelpad=6, fontsize=13, color=TEXT_PRIMARY)
    ax3d.set_ylabel("y", labelpad=6, fontsize=13, color=TEXT_PRIMARY)
    ax3d.set_zlabel("z = xy", labelpad=6, fontsize=13, color=TEXT_PRIMARY)
    ax3d.view_init(elev=25, azim=-50 + 35 * p)
    ax3d.xaxis.pane.fill = False
    ax3d.yaxis.pane.fill = False
    ax3d.zaxis.pane.fill = False
    ax3d.set_title(r"Unconstrained Surface: $z = f(x, y) = xy$", fontsize=17, color=TEXT_PRIMARY, pad=10)

    # Right explanation card
    draw_card(ov, 0.60, 0.14, 0.36, 0.72)
    ov.text(0.78, 0.80, "Unconstrained Optimization", ha="center", va="center",
            fontsize=21, fontweight="bold", color=COLOR_ACCENT)

    a1 = sub_progress(p, 0.05, 0.30)
    a2 = sub_progress(p, 0.28, 0.55)
    a3 = sub_progress(p, 0.55, 0.82)

    ov.text(0.63, 0.71, r"Objective:  $f(x, y) = xy$", ha="left", va="center",
            fontsize=19, color=TEXT_PRIMARY, alpha=a1)
    ov.text(0.63, 0.62, r"Set $\nabla f = \mathbf{0} \;\Rightarrow\; (y, x) = (0, 0)$",
            ha="left", va="center", fontsize=17, color=COLOR_TANGENT, alpha=a2)
    ov.text(0.63, 0.53, "• Origin (0, 0) is only a saddle point.", ha="left", va="center",
            fontsize=15.5, color=TEXT_SECONDARY, alpha=a2)

    draw_card(ov, 0.625, 0.22, 0.31, 0.22, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MIN, lw=1.6, alpha=a3)
    ov.text(0.78, 0.37, "No Finite Maximum!", ha="center", va="center",
            fontsize=18, fontweight="bold", color=COLOR_MIN, alpha=a3)
    ov.text(0.78, 0.29, r"As $x, y \to +\infty$,  $f(x, y) = xy \to +\infty$" + "\n" +
            r"As $x \to +\infty, y \to -\infty$,  $f \to -\infty$",
            ha="center", va="center", fontsize=14.5, color=TEXT_PRIMARY, alpha=a3)
    return fig


def render_s1_constrained_hook(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 1, "Scene 1 • Hook / Context", gp)

    ax = fig.add_axes([0.05, 0.11, 0.49, 0.76])
    setup_2d_math_axes(ax, lim=3.8)
    draw_constraint_circle(ax, radius=np.sqrt(8.0), lw=3.0)

    # Sweeping rectangle corner along Q1 from 15 deg to 75 deg and settling near 45 deg
    angle = np.deg2rad(16.0 + 58.0 * np.sin(np.pi * sub_progress(p, 0.05, 0.85)) ** 1.0)
    r = np.sqrt(8.0)
    cx, cy = r * np.cos(angle), r * np.sin(angle)
    rect = patches.Rectangle((-cx, -cy), 2 * cx, 2 * cy, facecolor=COLOR_ACCENT, alpha=0.20,
                             edgecolor=COLOR_ACCENT, lw=2.5, zorder=4)
    ax.add_patch(rect)
    ax.scatter([cx], [cy], color=COLOR_TANGENT, s=110, zorder=8)
    ax.text(cx + 0.18, cy + 0.22, f"({cx:.2f}, {cy:.2f})", color=COLOR_TANGENT, fontsize=13, fontweight="bold")

    # Origin marked as outside constraint
    ax.scatter([0], [0], color=COLOR_MIN, s=90, marker="x", lw=2.5, zorder=8)
    ax.text(0.15, -0.38, "(0, 0) not on circle!", color=COLOR_MIN, fontsize=12, fontweight="bold")
    ax.set_title(r"Inscribed Rectangle on $x^2 + y^2 = 8$", fontsize=17, color=TEXT_PRIMARY, pad=10)

    # Right panel
    draw_card(ov, 0.58, 0.14, 0.38, 0.72)
    ov.text(0.77, 0.80, "Adding a Real Constraint", ha="center", va="center",
            fontsize=21, fontweight="bold", color=COLOR_ACCENT)

    ov.text(0.61, 0.70, r"Constraint:  $g(x, y) = x^2 + y^2 - 8 = 0$",
            ha="left", va="center", fontsize=17, color=COLOR_CONSTRAINT)
    ov.text(0.61, 0.62, r"Radius:  $R = \sqrt{8} = 2\sqrt{2} \approx 2.83$",
            ha="left", va="center", fontsize=15.5, color=TEXT_SECONDARY)

    ov.text(0.61, 0.52, f"Live Corner:  x = {cx:.2f},  y = {cy:.2f}",
            ha="left", va="center", fontsize=16, color=COLOR_TANGENT)
    ov.text(0.61, 0.45, f"Rectangle Area = 4xy = {4*cx*cy:.2f}",
            ha="left", va="center", fontsize=17, fontweight="bold", color=COLOR_MAX)

    a_q = sub_progress(p, 0.40, 0.70)
    draw_card(ov, 0.605, 0.18, 0.33, 0.20, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_TANGENT, lw=1.8, alpha=a_q)
    ov.text(0.77, 0.32, "Guiding Question", ha="center", va="center",
            fontsize=17, fontweight="bold", color=COLOR_TANGENT, alpha=a_q)
    ov.text(0.77, 0.24, "How do we find the extrema of f(x, y)\nwhen forced to stay on g(x, y) = 0?",
            ha="center", va="center", fontsize=14.5, color=TEXT_PRIMARY, alpha=a_q)
    return fig


def render_s2_goal(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 2, "Scene 2 • Concept Introduction", gp)

    a1 = sub_progress(p, 0.0, 0.3)
    a2 = sub_progress(p, 0.25, 0.6)

    draw_card(ov, 0.06, 0.24, 0.50, 0.54, facecolor=PANEL_BG, edgecolor=COLOR_ACCENT, lw=2.0, alpha=a1)
    ov.text(0.31, 0.70, "Learning Objective", ha="center", va="center",
            fontsize=24, fontweight="bold", color=COLOR_ACCENT, alpha=a1)
    ov.plot([0.12, 0.50], [0.64, 0.64], color=PANEL_BORDER, lw=1.5, alpha=a1, zorder=4)

    wrapped = (
        "By the end of this video, you will be able to:\n\n"
        "1. Explain geometrically why constrained extrema\n"
        "    occur where level curves touch the constraint\n"
        "    curve tangentially (parallel gradients).\n\n"
        "2. Solve a two-variable constrained optimization\n"
        "    problem step by step using  ∇f = λ∇g."
    )
    ov.text(0.10, 0.44, wrapped, ha="left", va="center", fontsize=17, color=TEXT_PRIMARY, linespacing=1.45, alpha=a1)

    # Right preview visual: tangency teaser
    ax = fig.add_axes([0.60, 0.18, 0.35, 0.62])
    setup_2d_math_axes(ax, lim=3.6)
    draw_hyperbolas(ax, [1.5, 2.8, 4.0], highlight_k=4.0, alpha=0.65 * a2)
    draw_constraint_circle(ax, radius=np.sqrt(8.0), lw=3.0, alpha=a2)
    if a2 > 0.2:
        ax.scatter([2.0], [2.0], color=COLOR_MAX, s=120, zorder=10, alpha=a2)
        draw_arrow_2d(ax, (2, 2), (0.9, 0.9), COLOR_GRAD_F, r"$\nabla f$", (-0.28, 0.18), scale=1.0, alpha=a2)
        draw_arrow_2d(ax, (2, 2), (1.35, 1.35), COLOR_GRAD_G, r"$\lambda\nabla g$", (0.35, -0.15), lw=2.2, alpha=a2)
    ax.set_title(r"Preview: Tangency at $\nabla f = \lambda \nabla g$", fontsize=16, color=TEXT_PRIMARY, pad=10)
    return fig


def render_s2_definitions(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 2, "Scene 2 • Concept Introduction", gp)

    ov.text(0.50, 0.85, "Key Notation & Definitions", ha="center", va="center",
            fontsize=26, fontweight="bold", color=TEXT_PRIMARY)

    cards = [
        (0.06, 0.48, 0.42, 0.30, sub_progress(p, 0.02, 0.25), COLOR_ACCENT,
         "1. Objective Function",
         r"$f : \mathbb{R}^2 \to \mathbb{R}, \quad z = f(x, y)$",
         "Differentiable scalar quantity we want\nto maximize or minimize."),
        (0.52, 0.48, 0.42, 0.30, sub_progress(p, 0.22, 0.48), COLOR_CONSTRAINT,
         "2. Constraint Curve",
         r"$g(x, y) = c \;\;\Longleftrightarrow\;\; g(x, y) - c = 0$",
         "Differentiable curve restricting allowed\ninput pairs (x, y)."),
        (0.06, 0.12, 0.42, 0.30, sub_progress(p, 0.45, 0.70), COLOR_LEVEL,
         "3. Level Curve (Contour)",
         r"$f(x, y) = k \quad (k \in \mathbb{R}\ \mathrm{constant})$",
         "Set of points in the xy-plane where f\ntakes the exact same height k."),
        (0.52, 0.12, 0.42, 0.30, sub_progress(p, 0.68, 0.92), COLOR_GRAD_F,
         "4. Gradient Vector",
         r"$\nabla f(x,y) = \left[\frac{\partial f}{\partial x},\; \frac{\partial f}{\partial y}\right]^T$",
         "Always perpendicular to level curves;\npoints in direction of steepest increase."),
    ]
    for x, y, w, h, alpha, col, title, eq, desc in cards:
        draw_card(ov, x, y, w, h, facecolor=PANEL_BG, edgecolor=col, lw=1.8, alpha=alpha)
        ov.text(x + 0.025, y + h - 0.055, title, ha="left", va="center",
                fontsize=18, fontweight="bold", color=col, alpha=alpha)
        ov.text(x + w / 2, y + h * 0.50, eq, ha="center", va="center",
                fontsize=19, color=TEXT_PRIMARY, alpha=alpha)
        ov.text(x + 0.025, y + 0.065, desc, ha="left", va="center",
                fontsize=14, color=TEXT_SECONDARY, linespacing=1.35, alpha=alpha)
    return fig


def render_s2_theorem(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 2, "Scene 2 • Concept Introduction", gp)

    a1 = sub_progress(p, 0.0, 0.30)
    a2 = sub_progress(p, 0.30, 0.65)
    a3 = sub_progress(p, 0.60, 0.90)

    draw_card(ov, 0.10, 0.16, 0.80, 0.68, facecolor=PANEL_BG, edgecolor=COLOR_TANGENT, lw=2.2, alpha=a1)
    ov.text(0.50, 0.76, "Theorem: Method of Lagrange Multipliers", ha="center", va="center",
            fontsize=25, fontweight="bold", color=COLOR_TANGENT, alpha=a1)

    ov.text(
        0.50, 0.64,
        r"Suppose $f(x, y)$ attains a local extremum subject to $g(x, y) = c$ at $(x_0, y_0)$.",
        ha="center", va="center", fontsize=18.5, color=TEXT_PRIMARY, alpha=a1
    )
    ov.text(
        0.50, 0.55,
        r"If the regularity condition holds:  $\nabla g(x_0, y_0) \neq \mathbf{0}$,",
        ha="center", va="center", fontsize=18.5, color=COLOR_GRAD_G, alpha=a2
    )
    ov.text(
        0.50, 0.46,
        r"then there exists a scalar $\lambda \in \mathbb{R}$ (the Lagrange multiplier) such that:",
        ha="center", va="center", fontsize=17.5, color=TEXT_SECONDARY, alpha=a2
    )

    draw_card(ov, 0.22, 0.23, 0.56, 0.16, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_ACCENT, lw=2.2, alpha=a3)
    ov.text(
        0.50, 0.31,
        r"$\nabla f(x_0, y_0) = \lambda\,\nabla g(x_0, y_0) \qquad \mathrm{and} \qquad g(x_0, y_0) = c$",
        ha="center", va="center", fontsize=24, fontweight="bold", color=TEXT_PRIMARY, alpha=a3
    )
    return fig


def render_s3_slice3d(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 3, "Scene 3 • Visual Intuition", gp)

    ax3d = fig.add_axes([0.04, 0.06, 0.55, 0.77], projection="3d", facecolor=BG_COLOR)
    u = np.linspace(-3.3, 3.3, 44)
    X, Y = np.meshgrid(u, u)
    Z = X * Y
    ax3d.plot_surface(X, Y, Z, cmap="coolwarm", alpha=0.55, edgecolor="none")

    # Vertical cylinder x^2 + y^2 = 8
    cyl_alpha = 0.28 * sub_progress(p, 0.05, 0.45)
    if cyl_alpha > 0.01:
        th = np.linspace(0, 2 * np.pi, 72)
        zz = np.linspace(-7.5, 7.5, 14)
        TH, ZZ = np.meshgrid(th, zz)
        CX = np.sqrt(8.0) * np.cos(TH)
        CY = np.sqrt(8.0) * np.sin(TH)
        ax3d.plot_surface(CX, CY, ZZ, color="#FFFFFF", alpha=cyl_alpha, edgecolor="none")

    # Intersection curve traced progressively
    trace_p = sub_progress(p, 0.25, 0.85)
    if trace_p > 0.01:
        th_c = np.linspace(0, 2 * np.pi * trace_p, 240)
        rx = np.sqrt(8.0) * np.cos(th_c)
        ry = np.sqrt(8.0) * np.sin(th_c)
        rz = rx * ry
        ax3d.plot(rx, ry, rz, color=COLOR_TANGENT, lw=4.0, zorder=10)

    if p > 0.65:
        pk_a = sub_progress(p, 0.65, 0.90)
        ax3d.scatter([2, -2], [2, -2], [4, 4], color=COLOR_MAX, s=110, alpha=pk_a, zorder=12)
        ax3d.scatter([2, -2], [-2, 2], [-4, -4], color=COLOR_MIN, s=110, alpha=pk_a, zorder=12)

    ax3d.set_xlim(-3.4, 3.4)
    ax3d.set_ylim(-3.4, 3.4)
    ax3d.set_zlim(-9, 9)
    ax3d.set_xlabel("x", fontsize=12, color=TEXT_PRIMARY)
    ax3d.set_ylabel("y", fontsize=12, color=TEXT_PRIMARY)
    ax3d.set_zlabel("z = xy", fontsize=12, color=TEXT_PRIMARY)
    ax3d.view_init(elev=26, azim=-45 + 30 * p)
    ax3d.xaxis.pane.fill = False
    ax3d.yaxis.pane.fill = False
    ax3d.zaxis.pane.fill = False
    ax3d.set_title(r"Slicing $z = xy$ with Cylinder $x^2 + y^2 = 8$", fontsize=17, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.61, 0.16, 0.35, 0.68)
    ov.text(0.785, 0.78, "From 3D Surface to Constraint Path", ha="center", va="center",
            fontsize=19, fontweight="bold", color=COLOR_ACCENT)
    ov.text(
        0.635, 0.61,
        "• The vertical cylinder restricts\n  inputs (x, y) to the circle.\n\n"
        "• On the saddle surface, the\n  allowed path forms a closed\n  roller-coaster loop.",
        ha="left", va="center", fontsize=15.5, color=TEXT_PRIMARY, linespacing=1.4
    )
    a_pv = sub_progress(p, 0.55, 0.85)
    draw_card(ov, 0.635, 0.22, 0.30, 0.21, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MAX, lw=1.6, alpha=a_pv)
    ov.text(0.785, 0.37, "Two Peaks (+4) • Two Valleys (-4)", ha="center", va="center",
            fontsize=15.5, fontweight="bold", color=COLOR_MAX, alpha=a_pv)
    ov.text(0.785, 0.28, "Next: project flat onto the xy-plane\nto see why extrema occur here.",
            ha="center", va="center", fontsize=14, color=TEXT_SECONDARY, alpha=a_pv)
    return fig


def render_s3_contours_2d(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 3, "Scene 3 • Visual Intuition", gp)

    ax = fig.add_axes([0.05, 0.11, 0.49, 0.76])
    setup_2d_math_axes(ax, lim=4.0)

    all_levels = [-4, -2, 0, 1, 2, 3, 4]
    n_show = max(1, int(np.ceil(len(all_levels) * sub_progress(p, 0.15, 0.85))))
    draw_hyperbolas(ax, all_levels[:n_show], alpha=0.75)
    draw_constraint_circle(ax, radius=np.sqrt(8.0), lw=3.2)

    if n_show >= 4:
        ax.text(2.45, 0.42, "k = 1", color=COLOR_LEVEL, fontsize=11, fontweight="bold")
    if n_show >= 5:
        ax.text(2.75, 0.82, "k = 2", color=COLOR_LEVEL, fontsize=11, fontweight="bold")
    if n_show >= 7:
        ax.text(2.90, 1.45, "k = 4", color=COLOR_LEVEL, fontsize=11, fontweight="bold")

    ax.set_title(r"2D Top-Down View: Level Curves $xy = k$ & Circle", fontsize=17, color=TEXT_PRIMARY, pad=10)

    draw_card(ov, 0.58, 0.16, 0.38, 0.68)
    ov.text(0.77, 0.78, "Reading the Contour Map", ha="center", va="center",
            fontsize=21, fontweight="bold", color=COLOR_ACCENT)

    ov.plot([0.61, 0.66], [0.67, 0.67], color=COLOR_CONSTRAINT, lw=3.5, zorder=4)
    ov.text(0.68, 0.67, r"Constraint road: $x^2 + y^2 = 8$", ha="left", va="center",
            fontsize=15.5, color=TEXT_PRIMARY)

    ov.plot([0.61, 0.66], [0.58, 0.58], color=COLOR_LEVEL, lw=2.5, zorder=4)
    ov.text(0.68, 0.58, r"Level curves: $xy = k$ (solid $k>0$)", ha="left", va="center",
            fontsize=15.5, color=COLOR_LEVEL)

    ov.plot([0.61, 0.66], [0.50, 0.50], color=COLOR_LEVEL, lw=2.0, ls="--", zorder=4)
    ov.text(0.68, 0.50, r"Negative contours ($k<0$)", ha="left", va="center",
            fontsize=15.5, color=TEXT_SECONDARY)

    ov.text(
        0.61, 0.31,
        "Goal: walk ONLY along the white\n"
        "circle and find the highest and\n"
        "lowest contour lines k we can reach!",
        ha="left", va="center", fontsize=16, color=TEXT_PRIMARY, linespacing=1.45
    )
    return fig


def render_s3_crossing(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 3, "Scene 3 • Visual Intuition", gp)

    ax = fig.add_axes([0.05, 0.11, 0.49, 0.76])
    setup_2d_math_axes(ax, lim=3.8)
    r = np.sqrt(8.0)

    # Point at theta = 20 deg (or moving gently from 14 to 22 deg)
    theta = np.deg2rad(14.0 + 8.0 * sub_progress(p, 0.0, 0.35))
    px, py = r * np.cos(theta), r * np.sin(theta)
    k_val = px * py

    draw_hyperbolas(ax, [1.0, 2.0, 3.0, 4.0], highlight_k=None, alpha=0.35)
    # Draw current crossing level curve xy = k_val prominently
    xp = np.linspace(0.35, 3.7, 250)
    yp = k_val / xp
    m = yp <= 3.7
    ax.plot(xp[m], yp[m], color=COLOR_TANGENT, lw=2.4, alpha=0.85, zorder=4)
    draw_constraint_circle(ax, radius=r, lw=3.2)

    ax.scatter([px], [py], color="#FFFFFF", edgecolor=BG_COLOR, s=130, lw=2, zorder=10)
    ax.text(px + 0.16, py - 0.25, "P", color="#FFFFFF", fontsize=15, fontweight="bold", zorder=11)

    # Unit tangent T and gradient grad_f = (py, px)
    tx, ty = -np.sin(theta), np.cos(theta)
    gf = np.array([py, px])
    gf_u = gf / np.linalg.norm(gf) * 1.15
    T_vec = np.array([tx, ty]) * 1.15

    a_T = sub_progress(p, 0.18, 0.42)
    a_gf = sub_progress(p, 0.35, 0.62)
    a_proj = sub_progress(p, 0.58, 0.85)

    draw_arrow_2d(ax, (px, py), tuple(T_vec), COLOR_TANGENT, r"$\mathbf{T}$", (0.22, 0.12), lw=3.2, alpha=a_T)
    draw_arrow_2d(ax, (px, py), tuple(gf_u), COLOR_GRAD_F, r"$\nabla f$", (0.20, 0.16), lw=3.2, alpha=a_gf)

    # Projection of gf_u onto unit tangent (tx, ty)
    proj_len = float(np.dot(gf_u, np.array([tx, ty])))
    proj_vec = proj_len * np.array([tx, ty])
    if a_proj > 0.02:
        ax.plot(
            [px + gf_u[0], px + proj_vec[0]],
            [py + gf_u[1], py + proj_vec[1]],
            color=COLOR_TANGENT, ls="--", lw=1.8, alpha=a_proj, zorder=9
        )
        draw_arrow_2d(
            ax, (px, py), tuple(proj_vec), "#22D3EE",
            r"$\nabla f \cdot \mathbf{T} > 0$", (-0.75, -0.25), lw=3.4, alpha=a_proj, fontsize=13
        )

    ax.set_title("Case 1: Level Curve Crosses the Circle", fontsize=17, color=TEXT_PRIMARY, pad=10)

    # Right explanation card
    draw_card(ov, 0.58, 0.14, 0.38, 0.72)
    ov.text(0.77, 0.80, "Why Crossing ≠ Extremum", ha="center", va="center",
            fontsize=21, fontweight="bold", color=COLOR_MIN)

    ov.text(0.61, 0.70, f"At P:  k = xy = {k_val:.2f}", ha="left", va="center",
            fontsize=17, color=COLOR_TANGENT, fontweight="bold")
    ov.text(0.61, 0.61,
            r"• $\mathbf{T}$ = direction along the circle" + "\n" +
            r"• $\nabla f$ = direction of steepest ascent",
            ha="left", va="center", fontsize=15.5, color=TEXT_PRIMARY, linespacing=1.5)

    dot_val = float(np.dot(gf, np.array([tx, ty])))
    ov.text(0.61, 0.46,
            r"Directional derivative along circle:" + "\n" +
            rf"$D_{{\mathbf{{T}}}} f = \nabla f \cdot \mathbf{{T}} = +{dot_val:.2f} > 0$",
            ha="left", va="center", fontsize=16.5, color="#22D3EE", linespacing=1.45, alpha=a_proj)

    draw_card(ov, 0.605, 0.18, 0.33, 0.18, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MIN, lw=1.6, alpha=a_proj)
    ov.text(0.77, 0.27,
            "Step forward (+T) → f increases!\nStep backward (−T) → f decreases!\nSo P CANNOT be an extremum.",
            ha="center", va="center", fontsize=14.5, color=TEXT_PRIMARY, linespacing=1.4, alpha=a_proj)
    return fig


def render_s3_tangency(p: float, gp: float):
    fig, ov = new_canvas()
    draw_header_and_progress(ov, 3, "Scene 3 • Visual Intuition", gp)

    ax = fig.add_axes([0.05, 0.11, 0.49, 0.76])
    setup_2d_math_axes(ax, lim=3.8)
    r = np.sqrt(8.0)

    # Slide theta from 22 deg -> 45 deg cleanly
    slide = sub_progress(p, 0.10, 0.65)
    theta = np.deg2rad(22.0 + 23.0 * slide)
    px, py = r * np.cos(theta), r * np.sin(theta)
    k_val = px * py

    draw_hyperbolas(ax, [1.0, 2.0, 3.0], alpha=0.35)
    # Flash k=5 infeasible hyperbola briefly
    if 0.15 < p < 0.45:
        a5 = np.sin(np.pi * (p - 0.15) / 0.30)
        xp5 = np.linspace(1.35, 3.7, 150)
        yp5 = 5.0 / xp5
        m5 = yp5 <= 3.7
        ax.plot(xp5[m5], yp5[m5], color=COLOR_MIN, ls="--", lw=2.2, alpha=0.85 * a5)
        ax.text(2.6, 2.15, "k = 5 (misses circle!)", color=COLOR_MIN, fontsize=11.5, fontweight="bold", alpha=a5)

    # Current hyperbola xy = k_val
    xp = np.linspace(0.5, 3.7, 250)
    yp = k_val / xp
    m = yp <= 3.7
    ax.plot(xp[m], yp[m], color=COLOR_MAX if slide > 0.92 else COLOR_TANGENT, lw=2.8, zorder=4)
    draw_constraint_circle(ax, radius=r, lw=3.2)

    ax.scatter([px], [py], color=COLOR_MAX if slide > 0.92 else "#FFFFFF", edgecolor=BG_COLOR, s=140, lw=2, zorder=10)
    ax.text(px + 0.15, py - 0.25, "(2, 2)" if slide > 0.92 else "P", color=TEXT_PRIMARY, fontsize=14, fontweight="bold", zorder=11)

    tx, ty = -np.sin(theta), np.cos(theta)
    gf = np.array([py, px])
    gg = np.array([2 * px, 2 * py])
    gf_u = gf / np.linalg.norm(gf) * 1.15
    gg_u = gg / np.linalg.norm(gg) * 1.48  # slightly longer to distinguish visually when collinear
    T_vec = np.array([tx, ty]) * 1.05

    a_gg = sub_progress(p, 0.45, 0.72)
    draw_arrow_2d(ax, (px, py), tuple(T_vec), COLOR_TANGENT, r"$\mathbf{T}$", (-0.20, 0.20), lw=2.8)
    draw_arrow_2d(ax, (px, py), tuple(gg_u), COLOR_GRAD_G, r"$\nabla g$", (0.28, -0.05), lw=2.8, alpha=a_gg)
    draw_arrow_2d(ax, (px, py), tuple(gf_u), COLOR_GRAD_F, r"$\nabla f$", (-0.05, 0.28), lw=3.4)

    ax.set_title("Case 2: Curves Kiss Tangentially → Gradients Align!", fontsize=17, color=TEXT_PRIMARY, pad=10)

    # Right panel
    draw_card(ov, 0.58, 0.12, 0.38, 0.75)
    ov.text(0.77, 0.81, "The Tangency Condition", ha="center", va="center",
            fontsize=21, fontweight="bold", color=COLOR_MAX)

    dot_val = float(np.dot(gf, np.array([tx, ty])))
    ov.text(0.61, 0.72, f"Current height:  k = {k_val:.2f}", ha="left", va="center",
            fontsize=16.5, color=COLOR_TANGENT, fontweight="bold")
    ov.text(0.61, 0.65, rf"$\nabla f \cdot \mathbf{{T}} = {dot_val:.2f}$", ha="left", va="center",
            fontsize=16.5, color="#22D3EE")

    a_p1 = sub_progress(p, 0.50, 0.70)
    a_p2 = sub_progress(p, 0.65, 0.82)
    a_p3 = sub_progress(p, 0.78, 0.94)

    ov.text(0.61, 0.53, r"1. At extremum:  $\nabla f \cdot \mathbf{T} = 0\;\Rightarrow\;\nabla f \perp \mathbf{T}$",
            ha="left", va="center", fontsize=15, color=TEXT_PRIMARY, alpha=a_p1)
    ov.text(0.61, 0.44, r"2. On $g(x,y)=c$:  $\nabla g \cdot \mathbf{T} = 0\;\Rightarrow\;\nabla g \perp \mathbf{T}$",
            ha="left", va="center", fontsize=15, color=COLOR_GRAD_G, alpha=a_p2)

    draw_card(ov, 0.605, 0.16, 0.33, 0.21, facecolor=PANEL_HIGHLIGHT, edgecolor=COLOR_MAX, lw=2.0, alpha=a_p3)
    ov.text(0.77, 0.31, r"In $\mathbb{R}^2$, both $\perp \mathbf{T}$ $\Rightarrow$ Parallel!", ha="center", va="center",
            fontsize=16, fontweight="bold", color=COLOR_MAX, alpha=a_p3)
    ov.text(0.77, 0.22, r"$\nabla f = \lambda\,\nabla g$", ha="center", va="center",
            fontsize=24, fontweight="bold", color=TEXT_PRIMARY, alpha=a_p3)
    return fig

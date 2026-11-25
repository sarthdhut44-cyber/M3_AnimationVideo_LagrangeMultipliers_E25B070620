"""Single source of truth for the 6-scene storyboard, metadata, and timed narration beats."""

from dataclasses import dataclass
from typing import List


STUDENT_NAME = "Sarth Onkar Dhut"
STUDENT_URN = "E25B070620"
BATCH = "Turing"
LAB_BATCH = "Enigma"
COURSE = "Linear Algebra and Calculus (M3) • Internal Assessment"
VIDEO_TITLE = "Lagrange Multipliers: Why Parallel Gradients Solve Constrained Optimization"
CONCEPT = "Lagrange Multipliers (Constrained Optimization)"
LEARNING_OBJECTIVE = (
    "By the end of this video, the viewer will be able to explain geometrically why "
    "constrained extrema occur where the level curves of the objective function are "
    "tangent to the constraint curve (grad f = lambda grad g), and solve a two-variable "
    "constrained optimization problem step by step."
)


@dataclass(frozen=True)
class Beat:
    beat_id: str
    scene_num: int
    scene_name: str
    narration: str
    post_pause_sec: float = 0.55


BEATS: List[Beat] = [
    # --- SCENE 1: HOOK / CONTEXT (~38s) ---
    Beat(
        beat_id="s1_title",
        scene_num=1,
        scene_name="1. Hook / Context",
        narration=(
            "Welcome to this M3 Internal Assessment on Lagrange Multipliers, "
            "presented by Sarth Onkar Dhut, U R N, E 2 5 B 0 7 0 6 2 0."
        ),
        post_pause_sec=0.45,
    ),
    Beat(
        beat_id="s1_unconstrained",
        scene_num=1,
        scene_name="1. Hook / Context",
        narration=(
            "Suppose we want to maximize f of x, y equals x y. "
            "Without restrictions, this 3D saddle surface climbs endlessly upward, "
            "and the origin zero, zero is only a saddle point, so no finite maximum exists."
        ),
        post_pause_sec=0.4,
    ),
    Beat(
        beat_id="s1_constrained_hook",
        scene_num=1,
        scene_name="1. Hook / Context",
        narration=(
            "Now add a constraint: inscribe a rectangle inside a circle of radius square root of 8, "
            "keeping corner x, y on x squared plus y squared equals 8. "
            "Notice the origin isn't even on the circle! How do we optimize f when forced onto a curve?"
        ),
        post_pause_sec=0.5,
    ),

    # --- SCENE 2: CONCEPT INTRODUCTION (~40s) ---
    Beat(
        beat_id="s2_goal",
        scene_num=2,
        scene_name="2. Concept Introduction",
        narration=(
            "By the end of this video, you will understand geometrically why constrained extrema "
            "occur where level curves touch the constraint tangentially, and solve an example step by step."
        ),
        post_pause_sec=0.4,
    ),
    Beat(
        beat_id="s2_definitions",
        scene_num=2,
        scene_name="2. Concept Introduction",
        narration=(
            "Let us set up our notation. We have a differentiable objective f of x, y, "
            "and a differentiable constraint g of x, y equals c. "
            "A level curve is where f equals a constant k. "
            "The gradient nabla f contains partial f by partial x and partial f by partial y, "
            "always pointing perpendicular to level curves toward steepest ascent."
        ),
        post_pause_sec=0.45,
    ),
    Beat(
        beat_id="s2_theorem",
        scene_num=2,
        scene_name="2. Concept Introduction",
        narration=(
            "Lagrange's Theorem states: if f has a local extremum on g equals c at x naught, y naught "
            "where nabla g is nonzero, then there exists a scalar lambda such that "
            "nabla f equals lambda times nabla g, along with g equals c."
        ),
        post_pause_sec=0.5,
    ),

    # --- SCENE 3: VISUAL INTUITION (~80s) ---
    Beat(
        beat_id="s3_slice3d",
        scene_num=3,
        scene_name="3. Visual Intuition",
        narration=(
            "To see why, slice the saddle z equals x y with the vertical cylinder x squared plus y squared equals 8. "
            "Tracing around this circular path creates a loop with two peaks and two valleys."
        ),
        post_pause_sec=0.4,
    ),
    Beat(
        beat_id="s3_contours_2d",
        scene_num=3,
        scene_name="3. Visual Intuition",
        narration=(
            "Projecting onto the x y plane gives our white constraint circle "
            "overlaid with cyan level curves x y equals k."
        ),
        post_pause_sec=0.4,
    ),
    Beat(
        beat_id="s3_crossing",
        scene_num=3,
        scene_name="3. Visual Intuition",
        narration=(
            "Pick a point P where a level curve crosses the circle. "
            "Look at the yellow tangent T and the orange gradient nabla f. "
            "Because nabla f tilts across the circle, its projection along T is positive: "
            "nabla f dot T is greater than zero. "
            "Sliding forward increases f and stepping backward decreases f, so a crossing point cannot be an extremum."
        ),
        post_pause_sec=0.45,
    ),
    Beat(
        beat_id="s3_tangency",
        scene_num=3,
        scene_name="3. Visual Intuition",
        narration=(
            "Now slide P up to 2 comma 2, where k equals 4. Higher contours like k equals 5 miss the circle entirely. "
            "At 2 comma 2, the hyperbola just kisses the circle tangentially, so nabla f dot T equals zero. "
            "Because the circle is a level curve of g, nabla g dot T is also zero. "
            "In 2D, two vectors perpendicular to T must be parallel: nabla f equals lambda times nabla g!"
        ),
        post_pause_sec=0.55,
    ),

    # --- SCENE 4: WORKED EXAMPLE (~75s) ---
    Beat(
        beat_id="s4_setup",
        scene_num=4,
        scene_name="4. Worked Example",
        narration=(
            "Let us work through the algebra step by step for f equals x y on x squared plus y squared minus 8 equals zero. "
            "First compute both gradients: nabla f is y comma x, and nabla g is 2 x comma 2 y. "
            "Since nabla g equals zero only at the origin, which isn't on the circle, regularity holds everywhere."
        ),
        post_pause_sec=0.45,
    ),
    Beat(
        beat_id="s4_system",
        scene_num=4,
        scene_name="4. Worked Example",
        narration=(
            "Setting nabla f equal to lambda times nabla g yields three equations: "
            "y equals 2 lambda x, x equals 2 lambda y, and x squared plus y squared equals 8."
        ),
        post_pause_sec=0.4,
    ),
    Beat(
        beat_id="s4_solve",
        scene_num=4,
        scene_name="4. Worked Example",
        narration=(
            "Check for zero before dividing! If x were zero, equation one forces y equals zero, violating x squared plus y squared equals 8. "
            "So x and y are nonzero. Equating lambda gives y over 2 x equals x over 2 y, "
            "so y squared equals x squared, meaning y equals plus or minus x."
        ),
        post_pause_sec=0.45,
    ),
    Beat(
        beat_id="s4_candidates",
        scene_num=4,
        scene_name="4. Worked Example",
        narration=(
            "Substituting into the circle gives 2 x squared equals 8, so x equals plus or minus 2. "
            "This yields four candidates: 2 comma 2, minus 2 comma minus 2, 2 comma minus 2, and minus 2 comma 2. "
            "By the Extreme Value Theorem on this closed, bounded circle, global extrema must occur among these points."
        ),
        post_pause_sec=0.45,
    ),
    Beat(
        beat_id="s4_evaluate",
        scene_num=4,
        scene_name="4. Worked Example",
        narration=(
            "Evaluating f gives global maximum plus 4 at 2 comma 2 and minus 2 comma minus 2, with lambda equal to plus one-half; "
            "and global minimum minus 4 at 2 comma minus 2 and minus 2 comma 2, with lambda equal to minus one-half."
        ),
        post_pause_sec=0.5,
    ),

    # --- SCENE 5: INTERPRETATION (~40s) ---
    Beat(
        beat_id="s5_geometry",
        scene_num=5,
        scene_name="5. Interpretation",
        narration=(
            "Connecting back to geometry: at both maxima, lambda is positive one-half, so nabla f and nabla g point in the same outward direction. "
            "At both minima, lambda is negative one-half, so nabla f points opposite to nabla g."
        ),
        post_pause_sec=0.4,
    ),
    Beat(
        beat_id="s5_lambda_meaning",
        scene_num=5,
        scene_name="5. Interpretation",
        narration=(
            "Moreover, lambda measures sensitivity! On x squared plus y squared equals c, the maximum is f star equals c over 2, "
            "whose derivative d f star by d c is one-half, matching lambda. "
            "And for our inscribed rectangle, x equals 2, y equals 2 gives a 4 by 4 square with maximum area 16."
        ),
        post_pause_sec=0.5,
    ),

    # --- SCENE 6: SUMMARY & CREDITS (~28s) ---
    Beat(
        beat_id="s6_summary",
        scene_num=6,
        scene_name="6. Summary & Credits",
        narration=(
            "Three key takeaways: first, constrained extrema occur at tangency where nabla f equals lambda nabla g. "
            "Second, always verify regularity and zero edge cases. "
            "Third, lambda captures gradient alignment and constraint sensitivity."
        ),
        post_pause_sec=0.45,
    ),
    Beat(
        beat_id="s6_credits",
        scene_num=6,
        scene_name="6. Summary & Credits",
        narration=(
            "Thank you for watching. References, audio credits, and full AI disclosures are shown on screen "
            "and in the public GitHub repository."
        ),
        post_pause_sec=1.0,
    ),
]


SCENE_PLAN = [
    {
        "scene": "1. Hook / Context",
        "purpose": "Spark curiosity and motivate constrained optimization.",
        "visual": "3D saddle z = xy rising unboundedly; circular ring x^2+y^2 = 8 & inscribed rectangle problem.",
        "math": "Contrast unconstrained f(x,y)=xy (critical pt (0,0) off circle) vs. constrained optimization on g(x,y)=x^2+y^2-8=0.",
    },
    {
        "scene": "2. Concept Introduction",
        "purpose": "Define notation, learning goal, and Lagrange theorem.",
        "visual": "Clean typography cards introducing f, g, level curves, gradient vectors, and theorem statement.",
        "math": "grad f = [df/dx, df/dy], grad g = [dg/dx, dg/dy]; at extremum with grad g != 0, grad f = lambda * grad g and g(x,y) = c.",
    },
    {
        "scene": "3. Visual Intuition",
        "purpose": "Build geometric intuition before algebra.",
        "visual": "3D cylinder intersection curve -> 2D projection; animated point P walking circle with tangent T, grad f, and projection; crossing vs. kissing.",
        "math": "Directional derivative D_T f = grad f . T. Crossing => nonzero component along T. Tangency => grad f . T = 0 and grad g . T = 0 => grad f || grad g.",
    },
    {
        "scene": "4. Worked Example",
        "purpose": "Demonstrate complete step-by-step algebraic solution.",
        "visual": "Synchronized derivation panel beside live 2D curve highlighting candidate points (2,2), (-2,-2), (2,-2), (-2,2).",
        "math": "f(x,y)=xy, g(x,y)=x^2+y^2-8=0; grad f=(y,x), grad g=(2x,2y); check x!=0,y!=0; y^2=x^2 => x=+-2; EVT confirms global max +4, min -4.",
    },
    {
        "scene": "5. Interpretation",
        "purpose": "Connect final numbers and lambda back to geometry.",
        "visual": "All 4 extrema on 2D contour + 3D surface; same-direction vs opposite-direction arrows; expanding radius animation & inscribed 4x4 square.",
        "math": "lambda=+1/2 (max, parallel same sense), lambda=-1/2 (min, antiparallel); sensitivity df*/dc = 1/2 = lambda; max inscribed rectangle is 4x4 square (area 16).",
    },
    {
        "scene": "6. Summary & Credits",
        "purpose": "Reinforce 3 core takeaways and disclose tools/credits.",
        "visual": "3-card takeaway summary followed by Closing Frame with student details, references, music credit, and AI disclosure.",
        "math": "Key takeaways: (1) tangency <=> grad f = lambda grad g, (2) verify regularity & zero cases, (3) lambda = sensitivity df*/dc.",
    },
]

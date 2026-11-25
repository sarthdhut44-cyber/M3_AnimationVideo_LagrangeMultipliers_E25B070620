# Narration Script — Lagrange Multipliers: Why Parallel Gradients Solve Constrained Optimization

- **Student:** Sarth Onkar Dhut (`E25B070620`)
- **Batch / Lab Batch:** Turing / Enigma
- **Learning Objective:** By the end of this video, the viewer will be able to explain geometrically why constrained extrema occur where the level curves of the objective function are tangent to the constraint curve (grad f = lambda grad g), and solve a two-variable constrained optimization problem step by step.
- **Total Spoken Words:** 817

## Scene 1. Hook / Context

### `s1_title` (pause after: 0.45s)
Welcome to this M3 Internal Assessment on Lagrange Multipliers, presented by Sarth Onkar Dhut, U R N, E 2 5 B 0 7 0 6 2 0.

### `s1_unconstrained` (pause after: 0.40s)
Suppose we want to maximize f of x, y equals x y. Without restrictions, this 3D saddle surface climbs endlessly upward, and the origin zero, zero is only a saddle point, so no finite maximum exists.

### `s1_constrained_hook` (pause after: 0.50s)
Now add a constraint: inscribe a rectangle inside a circle of radius square root of 8, keeping corner x, y on x squared plus y squared equals 8. Notice the origin isn't even on the circle! How do we optimize f when forced onto a curve?

## Scene 2. Concept Introduction

### `s2_goal` (pause after: 0.40s)
By the end of this video, you will understand geometrically why constrained extrema occur where level curves touch the constraint tangentially, and solve an example step by step.

### `s2_definitions` (pause after: 0.45s)
Let us set up our notation. We have a differentiable objective f of x, y, and a differentiable constraint g of x, y equals c. A level curve is where f equals a constant k. The gradient nabla f contains partial f by partial x and partial f by partial y, always pointing perpendicular to level curves toward steepest ascent.

### `s2_theorem` (pause after: 0.50s)
Lagrange's Theorem states: if f has a local extremum on g equals c at x naught, y naught where nabla g is nonzero, then there exists a scalar lambda such that nabla f equals lambda times nabla g, along with g equals c.

## Scene 3. Visual Intuition

### `s3_slice3d` (pause after: 0.40s)
To see why, slice the saddle z equals x y with the vertical cylinder x squared plus y squared equals 8. Tracing around this circular path creates a loop with two peaks and two valleys.

### `s3_contours_2d` (pause after: 0.40s)
Projecting onto the x y plane gives our white constraint circle overlaid with cyan level curves x y equals k.

### `s3_crossing` (pause after: 0.45s)
Pick a point P where a level curve crosses the circle. Look at the yellow tangent T and the orange gradient nabla f. Because nabla f tilts across the circle, its projection along T is positive: nabla f dot T is greater than zero. Sliding forward increases f and stepping backward decreases f, so a crossing point cannot be an extremum.

### `s3_tangency` (pause after: 0.55s)
Now slide P up to 2 comma 2, where k equals 4. Higher contours like k equals 5 miss the circle entirely. At 2 comma 2, the hyperbola just kisses the circle tangentially, so nabla f dot T equals zero. Because the circle is a level curve of g, nabla g dot T is also zero. In 2D, two vectors perpendicular to T must be parallel: nabla f equals lambda times nabla g!

## Scene 4. Worked Example

### `s4_setup` (pause after: 0.45s)
Let us work through the algebra step by step for f equals x y on x squared plus y squared minus 8 equals zero. First compute both gradients: nabla f is y comma x, and nabla g is 2 x comma 2 y. Since nabla g equals zero only at the origin, which isn't on the circle, regularity holds everywhere.

### `s4_system` (pause after: 0.40s)
Setting nabla f equal to lambda times nabla g yields three equations: y equals 2 lambda x, x equals 2 lambda y, and x squared plus y squared equals 8.

### `s4_solve` (pause after: 0.45s)
Check for zero before dividing! If x were zero, equation one forces y equals zero, violating x squared plus y squared equals 8. So x and y are nonzero. Equating lambda gives y over 2 x equals x over 2 y, so y squared equals x squared, meaning y equals plus or minus x.

### `s4_candidates` (pause after: 0.45s)
Substituting into the circle gives 2 x squared equals 8, so x equals plus or minus 2. This yields four candidates: 2 comma 2, minus 2 comma minus 2, 2 comma minus 2, and minus 2 comma 2. By the Extreme Value Theorem on this closed, bounded circle, global extrema must occur among these points.

### `s4_evaluate` (pause after: 0.50s)
Evaluating f gives global maximum plus 4 at 2 comma 2 and minus 2 comma minus 2, with lambda equal to plus one-half; and global minimum minus 4 at 2 comma minus 2 and minus 2 comma 2, with lambda equal to minus one-half.

## Scene 5. Interpretation

### `s5_geometry` (pause after: 0.40s)
Connecting back to geometry: at both maxima, lambda is positive one-half, so nabla f and nabla g point in the same outward direction. At both minima, lambda is negative one-half, so nabla f points opposite to nabla g.

### `s5_lambda_meaning` (pause after: 0.50s)
Moreover, lambda measures sensitivity! On x squared plus y squared equals c, the maximum is f star equals c over 2, whose derivative d f star by d c is one-half, matching lambda. And for our inscribed rectangle, x equals 2, y equals 2 gives a 4 by 4 square with maximum area 16.

## Scene 6. Summary & Credits

### `s6_summary` (pause after: 0.45s)
Three key takeaways: first, constrained extrema occur at tangency where nabla f equals lambda nabla g. Second, always verify regularity and zero edge cases. Third, lambda captures gradient alignment and constraint sensitivity.

### `s6_credits` (pause after: 1.00s)
Thank you for watching. References, audio credits, and full AI disclosures are shown on screen and in the public GitHub repository.

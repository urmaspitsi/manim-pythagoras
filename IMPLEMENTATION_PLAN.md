# Pythagorean Shorts Implementation Plan

## Goal

Build a vertical YouTube Shorts animation in Manim that gives a playful, clear visual proof of the Pythagorean theorem in `75` seconds or less.

## Creative Direction

- Format: `9:16`
- Tone: playful explainer
- Style: bright background, bold colors, fast readable captions
- Proof choice: rearrangement proof using the same four congruent right triangles inside the same outer square

## Prototype Scope

The prototype focuses on one clean argument:

1. Introduce one right triangle and its side labels `a`, `b`, `c`.
2. Pack four copies into a large square, leaving a central `c²` region.
3. Rearrange the same four triangles into the same large square, now leaving `a²` and `b²`.
4. Conclude that the leftover areas must match, so `a² + b² = c²`.

## Technical Plan

1. Use a local `.venv` with Manim installed from an existing machine Python.
2. Keep the scene self-contained and avoid LaTeX dependencies by using `Text` instead of `MathTex`.
3. Force vertical output in the scene config so the render is always Shorts-oriented.
4. Use `imageio-ffmpeg` as the ffmpeg source so the project does not depend on a separate system ffmpeg install.
5. Render quickly at low quality first, then raise quality once timing and composition feel right.

## Recommendations For Next Iteration

- Add sound design cues for the triangle rearrangement.
- Replace static captions with word-by-word emphasis timed to narration.
- Add a faster hook in the first `2` seconds.
- Add a cleaner outro card with channel branding.
- Consider a second scene that overlays the algebra after the visual proof lands.


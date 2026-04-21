# Manim Pythagorean Shorts Prototype

This project contains a quick `9:16` Manim prototype for a playful YouTube Shorts style visual proof of the Pythagorean theorem.

## Render

```powershell
.\.venv\Scripts\manim.exe -ql shorts_pythagoras.py PythagoreanShortsPrototype
```

Use `-qm` or `-qh` when you want a cleaner export after iterating on the animation.

Or use the helper:

```powershell
.\render.ps1 low
.\render.ps1 medium
.\render.ps1 high
.\render.ps1 medium -Fresh
```

Use `-Fresh` when you want to force a full uncached render instead of reusing Manim's cached partials.
This helper also clears the scene's old partial render files and previous final MP4 before the fresh render starts.

## Files

- `shorts_pythagoras.py`: Main Manim scene
- `render.ps1`: Small render helper for low, medium, or high quality
- `IMPLEMENTATION_PLAN.md`: Current production plan
- `NARRATION.md`: Short voiceover draft matched to the prototype beats

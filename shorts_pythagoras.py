from __future__ import annotations

import os

import imageio_ffmpeg
import numpy as np

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    UP,
    AnimationGroup,
    Circle,
    Create,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    RoundedRectangle,
    Scene,
    Square,
    Succession,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    config,
)


FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
os.environ.setdefault("IMAGEIO_FFMPEG_EXE", FFMPEG_PATH)
config.ffmpeg_executable = FFMPEG_PATH
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30
config.background_color = "#0A0E16"

SURFACE = "#111722"
PANEL_FILL = "#121A26"
PANEL_STROKE = "#354253"
TEXT_PRIMARY = "#F5F0E8"
TEXT_SECONDARY = "#B5C0CE"
OUTLINE = "#E6E0D5"
TRIANGLE_COLORS = ["#17344C", "#1F435D", "#24586A", "#2F6A70"]
A_COLOR = "#6BAF7F"
B_COLOR = "#67AFC2"
C_COLOR = "#D8B46E"
ACCENT = "#9DA6B1"
MARKER_COLOR = "#C3CDD8"
FONT = "Palatino Linotype"
LAYOUT_SCALE = 1.12
LAYOUT_CENTER = UP * 0.32


class PythagoreanShortsPrototype(Scene):
    def construct(self) -> None:
        a = 3.0
        b = 2.0

        self.add(self.make_backdrop())

        header = self.make_header()
        caption = self.make_caption("Take one right triangle with legs a and b.")
        reference = self.make_reference_triangle(a, b)
        layout_one = self.make_layout_one(a, b)
        layout_two = self.make_layout_two(a, b)

        self.play(FadeIn(header, shift=UP * 0.2), FadeIn(caption, shift=UP * 0.12), run_time=1.0)
        self.play(
            LaggedStart(
                Create(reference["triangle"]),
                FadeIn(reference["right_angle"], shift=UP * 0.05),
                FadeIn(reference["labels"], shift=UP * 0.05),
                lag_ratio=0.14,
            ),
            run_time=1.8,
        )
        self.wait(0.35)

        next_caption = self.make_caption("Four congruent copies fit in a square of side a + b.")
        self.play(
            Succession(
                FadeOut(caption, shift=UP * 0.05),
                FadeIn(next_caption, shift=UP * 0.05),
            ),
            Create(layout_one["outer"]),
            FadeIn(layout_one["outer_labels"], shift=UP * 0.06),
            run_time=1.2,
        )
        caption = next_caption
        self.play(
            LaggedStart(
                *[TransformFromCopy(reference["triangle"], triangle) for triangle in layout_one["triangles"]],
                lag_ratio=0.12,
            ),
            FadeOut(reference["labels"], shift=DOWN * 0.08),
            FadeOut(reference["right_angle"], shift=DOWN * 0.08),
            run_time=2.2,
        )
        self.play(FadeOut(reference["triangle"], scale=0.92), run_time=0.3)

        triangles = VGroup(*layout_one["triangles"])
        self.wait(0.2)

        next_caption = self.make_caption("Each edge is c, and adjacent acute angles\nadd to 90 degrees, so the gap is a square.")
        self.play(
            Succession(
                FadeOut(caption, shift=UP * 0.05),
                FadeIn(next_caption, shift=UP * 0.05),
            ),
            DrawBorderThenFill(layout_one["center_square"]),
            FadeIn(layout_one["square_markers"], shift=UP * 0.04),
            FadeIn(layout_one["c_label"], shift=UP * 0.04),
            FadeIn(layout_one["center_label"], scale=0.92),
            run_time=1.9,
        )
        caption = next_caption
        self.wait(0.55)

        next_caption = self.make_caption("Now rearrange the same four triangles.")
        self.play(
            Succession(
                FadeOut(caption, shift=UP * 0.05),
                FadeIn(next_caption, shift=UP * 0.05),
            ),
            run_time=0.8,
        )
        caption = next_caption
        self.play(
            FadeOut(layout_one["center_square"]),
            FadeOut(layout_one["square_markers"]),
            FadeOut(layout_one["c_label"]),
            FadeOut(layout_one["center_label"]),
            run_time=0.45,
        )
        self.play(
            AnimationGroup(
                *[
                    Transform(triangles[index], layout_two["triangles"][index])
                    for index in range(4)
                ],
                lag_ratio=0.04,
            ),
            run_time=1.55,
        )

        next_caption = self.make_caption("The uncovered area is now a² plus b².")
        self.play(
            Succession(
                FadeOut(caption, shift=UP * 0.05),
                FadeIn(next_caption, shift=UP * 0.05),
            ),
            FadeIn(layout_two["a_square"]),
            FadeIn(layout_two["b_square"]),
            FadeIn(layout_two["a_label"], scale=0.9),
            FadeIn(layout_two["b_label"], scale=0.9),
            run_time=1.25,
        )
        caption = next_caption
        self.wait(0.5)

        proof_note = self.make_proof_note()
        proof_note.next_to(layout_one["outer"], DOWN, buff=0.24)

        equation = self.make_equation_panel()
        equation["group"].next_to(proof_note, DOWN, buff=0.22)

        next_caption = self.make_caption("The outer square stayed the same,\nand the four triangles stayed the same.")
        self.play(
            Succession(
                FadeOut(caption, shift=UP * 0.05),
                FadeIn(next_caption, shift=UP * 0.05),
            ),
            FadeIn(proof_note, shift=UP * 0.1),
            run_time=1.1,
        )
        caption = next_caption
        self.play(FadeIn(equation["panel"], scale=0.96), run_time=0.45)
        self.play(
            TransformFromCopy(layout_two["a_label"], equation["tokens"][0]),
            FadeIn(equation["tokens"][1], shift=UP * 0.04),
            TransformFromCopy(layout_two["b_label"], equation["tokens"][2]),
            FadeIn(equation["tokens"][3], shift=UP * 0.04),
            FadeIn(equation["tokens"][4], shift=UP * 0.04),
            run_time=1.35,
        )
        next_caption = self.make_caption("Therefore, a² + b² = c².")
        self.play(
            Succession(
                FadeOut(caption, shift=UP * 0.05),
                FadeIn(next_caption, shift=UP * 0.05),
            ),
            Indicate(equation["tokens"][4], color=C_COLOR, scale_factor=1.08),
            run_time=0.85,
        )
        caption = next_caption
        self.wait(1.7)

    def make_backdrop(self) -> VGroup:
        halo_left = Circle(radius=3.1, stroke_width=0, fill_color="#17304A", fill_opacity=0.12)
        halo_left.move_to(LEFT * 3.7 + UP * 5.35)

        halo_right = Circle(radius=2.75, stroke_width=0, fill_color="#173E4C", fill_opacity=0.1)
        halo_right.move_to(RIGHT * 2.8 + DOWN * 4.25)

        halo_bottom = Circle(radius=2.15, stroke_width=0, fill_color="#3A3148", fill_opacity=0.08)
        halo_bottom.move_to(LEFT * 2.35 + DOWN * 5.65)

        backdrop = VGroup(halo_left, halo_right, halo_bottom)
        backdrop.set_z_index(-20)
        return backdrop

    def make_header(self) -> VGroup:
        eyebrow = Text(
            "A classic rearrangement proof",
            font=FONT,
            font_size=21,
            color=ACCENT,
        )
        title = Text(
            "Why a² + b² = c²",
            font=FONT,
            font_size=48,
            color=TEXT_PRIMARY,
            weight="BOLD",
        )
        group = VGroup(eyebrow, title).arrange(DOWN, buff=0.15)
        group.to_edge(UP, buff=1.5)
        return group

    def make_caption(self, message: str) -> VGroup:
        label = Text(
            message,
            font=FONT,
            font_size=48,
            color=TEXT_PRIMARY,
            line_spacing=0.9,
        )
        label.scale_to_fit_width(8.15)
        panel = RoundedRectangle(
            corner_radius=0.16,
            width=min(8.55, label.width + 0.72),
            height=label.height + 0.46,
            fill_color=PANEL_FILL,
            fill_opacity=0.82,
            stroke_color=PANEL_STROKE,
            stroke_width=0,
        )
        label.move_to(panel.get_center())

        group = VGroup(panel, label)
        group.to_edge(DOWN, buff=2.42)
        return group

    def make_reference_triangle(self, a: float, b: float) -> dict[str, VGroup]:
        triangle = Polygon(
            np.array([-a / 2, -b / 2, 0.0]),
            np.array([a / 2, -b / 2, 0.0]),
            np.array([-a / 2, b / 2, 0.0]),
            stroke_color=OUTLINE,
            stroke_width=4,
            fill_color=TRIANGLE_COLORS[1],
            fill_opacity=0.94,
        )
        triangle.scale(0.9).move_to(UP * 1.18)

        vertices = triangle.get_vertices()
        right_angle = self.make_right_angle_marker(vertices[0], vertices[1], vertices[2], size=0.18, stroke_width=3.2)

        a_label = self.make_segment_label("a", vertices[0], vertices[1], color=A_COLOR, font_size=32, buff=0.22)
        b_label = self.make_segment_label("b", vertices[0], vertices[2], color=B_COLOR, font_size=32, buff=0.22)
        c_label = self.make_segment_label(
            "c",
            vertices[1],
            vertices[2],
            color=C_COLOR,
            font_size=32,
            buff=0.24,
            rotate_text=True,
            reference_point=triangle.get_center(),
        )
        labels = VGroup(a_label, b_label, c_label)
        labels.set_z_index(12)

        return {
            "triangle": triangle,
            "right_angle": right_angle,
            "labels": labels,
        }

    def make_layout_one(self, a: float, b: float) -> dict[str, object]:
        side_length = a + b
        outer = self.make_outer_square(side_length)

        triangles = [
            self.make_polygon([(0, 0), (a, 0), (0, b)], TRIANGLE_COLORS[0], side_length, outer),
            self.make_polygon([(a, 0), (side_length, 0), (side_length, a)], TRIANGLE_COLORS[1], side_length, outer),
            self.make_polygon(
                [(side_length, a), (side_length, side_length), (b, side_length)],
                TRIANGLE_COLORS[2],
                side_length,
                outer,
            ),
            self.make_polygon([(0, b), (0, side_length), (b, side_length)], TRIANGLE_COLORS[3], side_length, outer),
        ]

        center_square = self.make_polygon(
            [(a, 0), (side_length, a), (b, side_length), (0, b)],
            C_COLOR,
            side_length,
            outer,
            fill_opacity=0.26,
            stroke_width=3.2,
        )
        center_square.set_z_index(4)

        center_label = Text(
            "c²",
            font=FONT,
            font_size=41,
            color=C_COLOR,
            weight="BOLD",
        )
        center_label.move_to(center_square.get_center())
        center_label.set_z_index(8)

        center_vertices = center_square.get_vertices()
        square_markers = VGroup(
            *[
                self.make_right_angle_marker(
                    center_vertices[index],
                    center_vertices[index - 1],
                    center_vertices[(index + 1) % 4],
                    size=0.16,
                    stroke_width=2.6,
                )
                for index in range(4)
            ]
        )
        square_markers.set_z_index(7)

        c_label = self.make_segment_label(
            "c",
            center_vertices[0],
            center_vertices[1],
            color=C_COLOR,
            font_size=28,
            buff=0.24,
            rotate_text=True,
            reference_point=center_square.get_center(),
        )
        c_label.set_z_index(8)

        outer_top = Text(
            "a + b",
            font=FONT,
            font_size=27,
            color=TEXT_SECONDARY,
            weight="BOLD",
        )
        outer_top.next_to(outer, UP, buff=0.18)

        outer_side = Text(
            "a + b",
            font=FONT,
            font_size=27,
            color=TEXT_SECONDARY,
            weight="BOLD",
        )
        outer_side.rotate(PI / 2)
        outer_side.next_to(outer, RIGHT, buff=0.18)

        outer_labels = VGroup(outer_top, outer_side)
        outer_labels.set_z_index(15)

        return {
            "outer": outer,
            "outer_labels": outer_labels,
            "triangles": triangles,
            "center_square": center_square,
            "center_label": center_label,
            "c_label": c_label,
            "square_markers": square_markers,
        }

    def make_layout_two(self, a: float, b: float) -> dict[str, object]:
        side_length = a + b
        outer = self.make_outer_square(side_length)

        triangles = [
            self.make_polygon([(a, 0), (side_length, 0), (side_length, a)], TRIANGLE_COLORS[0], side_length, outer),
            self.make_polygon([(a, 0), (side_length, a), (a, a)], TRIANGLE_COLORS[1], side_length, outer),
            self.make_polygon([(0, a), (a, a), (0, side_length)], TRIANGLE_COLORS[2], side_length, outer),
            self.make_polygon([(a, a), (a, side_length), (0, side_length)], TRIANGLE_COLORS[3], side_length, outer),
        ]

        b_square = self.make_polygon(
            [(a, a), (side_length, a), (side_length, side_length), (a, side_length)],
            B_COLOR,
            side_length,
            outer,
            fill_opacity=0.3,
            stroke_width=3.2,
        )
        b_square.set_z_index(3)

        a_square = self.make_polygon(
            [(0, 0), (a, 0), (a, a), (0, a)],
            A_COLOR,
            side_length,
            outer,
            fill_opacity=0.3,
            stroke_width=3.2,
        )
        a_square.set_z_index(3)

        b_label = Text(
            "b²",
            font=FONT,
            font_size=38,
            color=B_COLOR,
            weight="BOLD",
        )
        b_label.move_to(b_square.get_center())
        b_label.set_z_index(8)

        a_label = Text(
            "a²",
            font=FONT,
            font_size=38,
            color=A_COLOR,
            weight="BOLD",
        )
        a_label.move_to(a_square.get_center())
        a_label.set_z_index(8)

        return {
            "outer": outer,
            "triangles": triangles,
            "a_square": a_square,
            "b_square": b_square,
            "a_label": a_label,
            "b_label": b_label,
        }

    def make_proof_note(self) -> VGroup:
        text = Text(
            "Same outer square. Same four triangles. Same leftover area.",
            font=FONT,
            font_size=22,
            color=TEXT_SECONDARY,
        )
        return VGroup(text)

    def make_equation_panel(self) -> dict[str, object]:
        tokens = VGroup(
            Text("a²", font=FONT, font_size=42, color=A_COLOR, weight="BOLD"),
            Text("+", font=FONT, font_size=42, color=TEXT_PRIMARY, weight="BOLD"),
            Text("b²", font=FONT, font_size=42, color=B_COLOR, weight="BOLD"),
            Text("=", font=FONT, font_size=42, color=TEXT_PRIMARY, weight="BOLD"),
            Text("c²", font=FONT, font_size=42, color=C_COLOR, weight="BOLD"),
        )
        tokens.arrange(RIGHT, buff=0.16)

        panel = RoundedRectangle(
            corner_radius=0.26,
            width=tokens.width + 0.86,
            height=tokens.height + 0.58,
            fill_color=PANEL_FILL,
            fill_opacity=0.88,
            stroke_color=PANEL_STROKE,
            stroke_width=0,
        )
        tokens.move_to(panel.get_center())

        group = VGroup(panel, tokens)
        return {"group": group, "panel": panel, "tokens": tokens}

    def make_outer_square(self, side_length: float) -> Square:
        outer = Square(
            side_length=side_length,
            stroke_color=OUTLINE,
            stroke_width=3.2,
            fill_color=SURFACE,
            fill_opacity=0.58,
        )
        outer.scale(LAYOUT_SCALE).move_to(LAYOUT_CENTER)
        outer.set_z_index(1)
        return outer

    def make_polygon(
        self,
        points: list[tuple[float, float]],
        fill_color: str,
        side_length: float,
        outer_square: Square,
        fill_opacity: float = 0.94,
        stroke_width: float = 4.0,
    ) -> Polygon:
        polygon = Polygon(
            *[self.to_scene_point(x, y, side_length) for x, y in points],
            stroke_color=OUTLINE,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )
        polygon.scale(LAYOUT_SCALE, about_point=ORIGIN)
        polygon.shift(outer_square.get_center())
        polygon.set_z_index(5)
        return polygon

    def make_right_angle_marker(
        self,
        vertex: np.ndarray,
        point_a: np.ndarray,
        point_b: np.ndarray,
        size: float = 0.16,
        stroke_width: float = 3.0,
    ) -> VGroup:
        direction_a = self.unit(point_a - vertex)
        direction_b = self.unit(point_b - vertex)
        corner = vertex + (direction_a + direction_b) * size

        marker = VGroup(
            Line(vertex + direction_a * size, corner, color=MARKER_COLOR, stroke_width=stroke_width),
            Line(vertex + direction_b * size, corner, color=MARKER_COLOR, stroke_width=stroke_width),
        )
        return marker

    def make_segment_label(
        self,
        text: str,
        start: np.ndarray,
        end: np.ndarray,
        color: str,
        font_size: float,
        buff: float,
        rotate_text: bool = False,
        reference_point: np.ndarray | None = None,
    ) -> Text:
        direction = end - start
        midpoint = (start + end) / 2
        normal = self.unit(np.array([-direction[1], direction[0], 0.0]))

        if reference_point is not None and np.dot(midpoint - reference_point, normal) < 0:
            normal *= -1

        label = Text(text, font=FONT, font_size=font_size, color=color, weight="BOLD")

        if rotate_text:
            angle = float(np.arctan2(direction[1], direction[0]))
            if angle > PI / 2:
                angle -= PI
            if angle < -PI / 2:
                angle += PI
            label.rotate(angle)

        label.move_to(midpoint + normal * buff)
        return label

    def to_scene_point(self, x: float, y: float, side_length: float) -> np.ndarray:
        return np.array([x - side_length / 2, y - side_length / 2, 0.0])

    def unit(self, vector: np.ndarray) -> np.ndarray:
        length = np.linalg.norm(vector)
        if length == 0:
            return vector
        return vector / length

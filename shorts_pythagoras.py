from __future__ import annotations

import os
import numpy as np
import imageio_ffmpeg

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    UP,
    AnimationGroup,
    Create,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    ReplacementTransform,
    RoundedRectangle,
    Scene,
    Square,
    Text,
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
config.background_color = "#FFF6E8"

TEXT_DARK = "#183153"
OUTLINE = "#20405D"
TRIANGLE_COLORS = ["#FF7A59", "#2EC4B6", "#FFD166", "#5E60CE"]
A_COLOR = "#FFB703"
B_COLOR = "#7BDFF2"
C_COLOR = "#EF476F"

FONT = "Trebuchet MS"


class PythagoreanShortsPrototype(Scene):
    def construct(self) -> None:
        a = 3.0
        b = 2.0

        title_card = self.make_title_card()
        self.play(FadeIn(title_card, shift=UP * 0.35), run_time=1.0)
        self.wait(0.6)

        header = self.make_header()
        self.play(ReplacementTransform(title_card, header), run_time=0.8)

        caption = self.make_caption("Start with one right triangle.")
        reference_triangle = self.make_reference_triangle(a, b)
        self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)
        self.play(
            LaggedStart(
                Create(reference_triangle["triangle"]),
                FadeIn(reference_triangle["right_angle"]),
                FadeIn(reference_triangle["labels"]),
                lag_ratio=0.18,
            ),
            run_time=1.8,
        )
        self.wait(1.0)

        layout_one = self.make_layout_one(a, b)
        self.play(
            ReplacementTransform(caption, self.make_caption("Pack 4 copies into a square of side a + b.")),
            FadeOut(reference_triangle["group"], shift=UP * 0.25),
            FadeIn(layout_one["outer_label"], shift=UP * 0.2),
            FadeIn(layout_one["outer"], shift=DOWN * 0.15),
            run_time=1.0,
        )
        self.play(
            LaggedStart(
                *[FadeIn(triangle, scale=0.96) for triangle in layout_one["triangles"]],
                lag_ratio=0.08,
            ),
            run_time=1.4,
        )
        self.wait(0.6)

        self.play(
            ReplacementTransform(caption, self.make_caption("The middle gap is a tilted square with area c².")),
            DrawBorderThenFill(layout_one["center_square"]),
            FadeIn(layout_one["c_side_label"], scale=0.85),
            FadeIn(layout_one["center_label"], scale=0.85),
            run_time=1.4,
        )
        self.play(Indicate(layout_one["center_label"], color=C_COLOR, scale_factor=1.1), run_time=0.8)
        self.wait(0.8)

        layout_two = self.make_layout_two(a, b)
        self.play(
            ReplacementTransform(caption, self.make_caption("Now rearrange the SAME 4 triangles.")),
            run_time=0.8,
        )
        self.play(
            AnimationGroup(
                *[
                    layout_one["triangles"][0].animate(path_arc=-PI / 10).become(layout_two["triangles"][0]),
                    layout_one["triangles"][1].animate(path_arc=PI / 9).become(layout_two["triangles"][1]),
                    layout_one["triangles"][2].animate(path_arc=-PI / 12).become(layout_two["triangles"][2]),
                    layout_one["triangles"][3].animate(path_arc=PI / 11).become(layout_two["triangles"][3]),
                ],
                lag_ratio=0.05,
            ),
            FadeOut(layout_one["center_square"]),
            FadeOut(layout_one["c_side_label"]),
            FadeOut(layout_one["center_label"]),
            FadeIn(layout_two["a_square"]),
            FadeIn(layout_two["b_square"]),
            run_time=2.4,
        )
        self.play(
            ReplacementTransform(caption, self.make_caption("Now the empty space is a² and b².")),
            FadeIn(layout_two["a_label"], scale=0.9),
            FadeIn(layout_two["b_label"], scale=0.9),
            run_time=1.0,
        )
        self.wait(1.0)

        proof_text = Text(
            "Same outer square. Same 4 triangles.",
            font=FONT,
            font_size=26,
            color=TEXT_DARK,
            weight="BOLD",
        )
        proof_text.next_to(layout_two["outer"], DOWN, buff=0.35)
        self.play(
            ReplacementTransform(caption, self.make_caption("So the leftover areas must be equal.")),
            FadeIn(proof_text, shift=UP * 0.2),
            run_time=1.0,
        )

        equation = self.make_equation()
        equation.next_to(proof_text, DOWN, buff=0.25)
        self.play(FadeIn(equation, shift=UP * 0.2), run_time=1.0)
        self.play(Indicate(equation[0], color=C_COLOR, scale_factor=1.08), run_time=0.8)
        self.wait(1.8)

    def make_title_card(self) -> VGroup:
        eyebrow = Text(
            "Pythagorean Theorem",
            font=FONT,
            font_size=28,
            color="#E76F51",
            weight="BOLD",
        )
        headline = Text(
            "Why does a² + b² = c²?",
            font=FONT,
            font_size=44,
            color=TEXT_DARK,
            weight="BOLD",
        )
        subtitle = Text(
            "A visual proof in one short",
            font=FONT,
            font_size=28,
            color="#47657B",
        )
        group = VGroup(eyebrow, headline, subtitle).arrange(DOWN, buff=0.14)
        group.move_to(UP * 5.0)
        return group

    def make_header(self) -> VGroup:
        chip = RoundedRectangle(
            corner_radius=0.25,
            width=6.5,
            height=0.85,
            fill_color="#FFFFFF",
            fill_opacity=0.92,
            stroke_color="#F4C38A",
            stroke_width=2,
        )
        text = Text(
            "Visual Proof of a² + b² = c²",
            font=FONT,
            font_size=28,
            color=TEXT_DARK,
            weight="BOLD",
        )
        text.move_to(chip.get_center())
        group = VGroup(chip, text)
        group.to_edge(UP, buff=0.35)
        return group

    def make_caption(self, message: str) -> VGroup:
        label = Text(
            message,
            font=FONT,
            font_size=28,
            color=TEXT_DARK,
            weight="BOLD",
        )
        panel = RoundedRectangle(
            corner_radius=0.22,
            width=min(8.2, label.width + 0.8),
            height=label.height + 0.42,
            fill_color="#FFFFFF",
            fill_opacity=0.94,
            stroke_color="#F4C38A",
            stroke_width=2,
        )
        label.move_to(panel.get_center())
        group = VGroup(panel, label)
        group.to_edge(DOWN, buff=0.45)
        return group

    def make_reference_triangle(self, a: float, b: float) -> dict[str, VGroup]:
        triangle = Polygon(
            np.array([-a / 2, -b / 2, 0]),
            np.array([a / 2, -b / 2, 0]),
            np.array([-a / 2, b / 2, 0]),
            stroke_color=OUTLINE,
            stroke_width=5,
            fill_color="#FFE3D3",
            fill_opacity=0.95,
        )
        triangle.scale(0.7).move_to(UP * 1.15)

        right_corner = triangle.get_vertices()[0]
        right_angle = VGroup(
            Line(right_corner + RIGHT * 0.18, right_corner + RIGHT * 0.18 + UP * 0.18, color=OUTLINE, stroke_width=4),
            Line(right_corner + UP * 0.18, right_corner + RIGHT * 0.18 + UP * 0.18, color=OUTLINE, stroke_width=4),
        )

        vertices = triangle.get_vertices()
        a_label = Text("a", font=FONT, font_size=34, color=TEXT_DARK, weight="BOLD").next_to(
            Line(vertices[0], vertices[1]), DOWN, buff=0.15
        )
        b_label = Text("b", font=FONT, font_size=34, color=TEXT_DARK, weight="BOLD").next_to(
            Line(vertices[0], vertices[2]), LEFT, buff=0.15
        )
        c_label = Text("c", font=FONT, font_size=34, color=TEXT_DARK, weight="BOLD").next_to(
            Line(vertices[1], vertices[2]), RIGHT, buff=0.15
        )
        labels = VGroup(a_label, b_label, c_label)
        group = VGroup(triangle, right_angle, labels)
        return {"triangle": triangle, "right_angle": right_angle, "labels": labels, "group": group}

    def make_layout_one(self, a: float, b: float) -> dict[str, object]:
        s = a + b
        outer = Square(side_length=s, stroke_color=OUTLINE, stroke_width=5)
        outer.scale(0.86).move_to(DOWN * 0.5)

        triangles = [
            self.make_polygon([(0, 0), (a, 0), (0, b)], TRIANGLE_COLORS[0], s, outer),
            self.make_polygon([(a, 0), (s, 0), (s, b)], TRIANGLE_COLORS[1], s, outer),
            self.make_polygon([(b, s), (s, s), (s, b)], TRIANGLE_COLORS[2], s, outer),
            self.make_polygon([(0, a), (0, s), (b, s)], TRIANGLE_COLORS[3], s, outer),
        ]

        center_square = self.make_polygon(
            [(a, 0), (s, b), (b, s), (0, a)],
            C_COLOR,
            s,
            outer,
            fill_opacity=0.28,
            stroke_width=4,
        )
        center_label = Text("c²", font=FONT, font_size=40, color=C_COLOR, weight="BOLD")
        center_label.move_to(center_square.get_center())
        center_vertices = center_square.get_vertices()
        c_edge = Line(center_vertices[0], center_vertices[1])
        c_side_label = Text("c", font=FONT, font_size=26, color=C_COLOR, weight="BOLD")
        c_side_label.rotate(c_edge.get_angle())
        c_side_label.move_to(c_edge.get_center() + UP * 0.28 + LEFT * 0.06)

        outer_label = Text("a + b", font=FONT, font_size=28, color=TEXT_DARK, weight="BOLD")
        outer_label.next_to(outer, UP, buff=0.2)

        return {
            "outer": outer,
            "triangles": triangles,
            "center_square": center_square,
            "center_label": center_label,
            "c_side_label": c_side_label,
            "outer_label": outer_label,
        }

    def make_layout_two(self, a: float, b: float) -> dict[str, object]:
        s = a + b
        outer = Square(side_length=s, stroke_color=OUTLINE, stroke_width=5)
        outer.scale(0.86).move_to(DOWN * 0.5)

        triangles = [
            self.make_polygon([(0, 0), (b, 0), (b, a)], TRIANGLE_COLORS[0], s, outer),
            self.make_polygon([(0, 0), (0, a), (b, a)], TRIANGLE_COLORS[1], s, outer),
            self.make_polygon([(b, a), (s, a), (s, s)], TRIANGLE_COLORS[2], s, outer),
            self.make_polygon([(b, a), (b, s), (s, s)], TRIANGLE_COLORS[3], s, outer),
        ]

        a_square = self.make_polygon(
            [(b, 0), (s, 0), (s, a), (b, a)],
            A_COLOR,
            s,
            outer,
            fill_opacity=0.3,
            stroke_width=4,
        )
        b_square = self.make_polygon(
            [(0, a), (b, a), (b, s), (0, s)],
            B_COLOR,
            s,
            outer,
            fill_opacity=0.3,
            stroke_width=4,
        )

        a_label = Text("a²", font=FONT, font_size=38, color=A_COLOR, weight="BOLD").move_to(a_square.get_center())
        b_label = Text("b²", font=FONT, font_size=38, color=B_COLOR, weight="BOLD").move_to(b_square.get_center())

        return {
            "outer": outer,
            "triangles": triangles,
            "a_square": a_square,
            "b_square": b_square,
            "a_label": a_label,
            "b_label": b_label,
        }

    def make_equation(self) -> VGroup:
        tokens = [
            Text("c²", font=FONT, font_size=40, color=C_COLOR, weight="BOLD"),
            Text("=", font=FONT, font_size=40, color=TEXT_DARK, weight="BOLD"),
            Text("a²", font=FONT, font_size=40, color=A_COLOR, weight="BOLD"),
            Text("+", font=FONT, font_size=40, color=TEXT_DARK, weight="BOLD"),
            Text("b²", font=FONT, font_size=40, color=B_COLOR, weight="BOLD"),
        ]
        group = VGroup(*tokens).arrange(RIGHT, buff=0.18)
        return group

    def make_polygon(
        self,
        points: list[tuple[float, float]],
        fill_color: str,
        side_length: float,
        outer_square: Square,
        fill_opacity: float = 0.94,
        stroke_width: float = 5,
    ) -> Polygon:
        base_points = [self.to_scene_point(x, y, side_length) for x, y in points]
        polygon = Polygon(
            *base_points,
            stroke_color=OUTLINE,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )
        polygon.scale(0.86)
        polygon.move_to(polygon.get_center() + outer_square.get_center())
        return polygon

    def to_scene_point(self, x: float, y: float, side_length: float) -> np.ndarray:
        return np.array([x - side_length / 2, y - side_length / 2, 0.0])

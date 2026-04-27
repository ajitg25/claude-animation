import math
import random

# Cocoa coords: origin bottom-left, Y increases upward
# Canvas: 900 x 500.  Handle sits top-left ~(140, 370).
# Whip extends rightward; tip arcs from coiled → S-curve → crack.

FRAMES: list[dict] = [
    dict(
        p0=(140, 370), p1=(178, 315), p2=(165, 215), p3=(170, 118),
        ms=620, crack=False, col=(0.78, 0.47, 0.22), lw=5,
    ),
    dict(
        p0=(140, 370), p1=(92, 405), p2=(82, 282), p3=(108, 152),
        ms=330, crack=False, col=(0.78, 0.47, 0.22), lw=5,
    ),
    dict(
        p0=(140, 342), p1=(238, 398), p2=(358, 278), p3=(388, 240),
        ms=110, crack=False, col=(0.84, 0.57, 0.34), lw=4,
    ),
    dict(
        p0=(140, 302), p1=(328, 400), p2=(508, 258), p3=(618, 278),
        ms=72, crack=False, col=(0.91, 0.76, 0.56), lw=3,
    ),
    dict(
        p0=(140, 282), p1=(378, 402), p2=(532, 162), p3=(748, 282),
        ms=52, crack=False, col=(0.97, 0.88, 0.72), lw=2,
    ),
    dict(
        p0=(140, 282), p1=(378, 402), p2=(532, 162), p3=(768, 282),
        ms=980, crack=True, col=(1.0, 1.0, 1.0), lw=2,
    ),
    dict(
        p0=(140, 282), p1=(308, 248), p2=(378, 322), p3=(458, 282),
        ms=520, crack=False, col=(0.78, 0.47, 0.22), lw=4,
    ),
]


def spark_lines(cx: float, cy: float) -> list[tuple]:
    rng = random.Random(42)
    lines = []
    for _ in range(16):
        angle = rng.uniform(0, 2 * math.pi)
        length = rng.uniform(35, 90)
        lines.append((cx, cy, cx + length * math.cos(angle), cy + length * math.sin(angle)))
    return lines

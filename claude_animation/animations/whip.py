import math

# Each frame: bezier control points, hold duration (ms), whether to show crack effect
FRAMES = [
    {
        'p0': (120, 120), 'p1': (160, 170), 'p2': (150, 260), 'p3': (155, 350),
        'ms': 600, 'crack': False, 'color': '#C87B3A', 'width': 5,
        'label': ('*winding up...*', '#555555', 13),
    },
    {
        'p0': (120, 120), 'p1': (75, 75), 'p2': (65, 190), 'p3': (95, 290),
        'ms': 320, 'crack': False, 'color': '#C87B3A', 'width': 5,
        'label': None,
    },
    {
        'p0': (120, 150), 'p1': (230, 75), 'p2': (340, 190), 'p3': (370, 225),
        'ms': 110, 'crack': False, 'color': '#D4925A', 'width': 4,
        'label': None,
    },
    {
        'p0': (120, 170), 'p1': (310, 75), 'p2': (490, 210), 'p3': (590, 188),
        'ms': 75, 'crack': False, 'color': '#E8C090', 'width': 3,
        'label': None,
    },
    {
        'p0': (120, 188), 'p1': (360, 82), 'p2': (510, 298), 'p3': (710, 188),
        'ms': 55, 'crack': False, 'color': '#F5DEB3', 'width': 2,
        'label': None,
    },
    {
        'p0': (120, 188), 'p1': (360, 82), 'p2': (510, 298), 'p3': (730, 188),
        'ms': 950, 'crack': True, 'color': '#FFFFFF', 'width': 2,
        'label': ('CRACK!', '#FF3300', 32),
    },
    {
        'p0': (120, 188), 'p1': (290, 230), 'p2': (370, 145), 'p3': (440, 188),
        'ms': 500, 'crack': False, 'color': '#C87B3A', 'width': 4,
        'label': ('*crack echoes...*', '#444444', 13),
    },
]


def bezier_points(p0, p1, p2, p3, steps=80):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        x = u**3*p0[0] + 3*u**2*t*p1[0] + 3*u*t**2*p2[0] + t**3*p3[0]
        y = u**3*p0[1] + 3*u**2*t*p1[1] + 3*u*t**2*p2[1] + t**3*p3[1]
        pts.extend([x, y])
    return pts


def spark_lines(cx, cy, seed=42):
    import random
    rng = random.Random(seed)
    lines = []
    for _ in range(14):
        angle = rng.uniform(0, 2 * math.pi)
        length = rng.uniform(25, 70)
        lines.append((cx, cy, cx + length * math.cos(angle), cy + length * math.sin(angle)))
    return lines

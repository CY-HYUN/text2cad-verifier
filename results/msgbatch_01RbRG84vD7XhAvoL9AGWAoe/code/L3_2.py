import cadquery as cq
import math

L, W, T = 100.0, 50.0, 3.0
A, lam, off, th = 5.0, 20.0, 5.0, 1.0
N = 401

top, bot = [], []
for i in range(N):
    x = L * i / (N - 1)
    y = A * math.sin(2 * math.pi * x / lam) + off
    d = A * (2 * math.pi / lam) * math.cos(2 * math.pi * x / lam)
    m = math.sqrt(1 + d * d)
    nx, ny = -d / m, 1 / m
    top.append((x + 0.5 * th * nx, y + 0.5 * th * ny))
    bot.append((x - 0.5 * th * nx, y - 0.5 * th * ny))

bot_rev = bot[::-1]
fin = (
    cq.Workplane("XY")
    .moveTo(*top[0])
    .spline(top[1:], includeCurrent=True)
    .lineTo(*bot_rev[0])
    .spline(bot_rev[1:], includeCurrent=True)
    .close()
    .extrude(W)
)

# trim fin ends to base length
trim = cq.Workplane("XY").box(L, 30, W, centered=False).translate((0, -5, 0))
fin = fin.intersect(trim)

base = cq.Workplane("XY").box(L, T, W, centered=False).translate((0, -T, 0))

result = base.union(fin)

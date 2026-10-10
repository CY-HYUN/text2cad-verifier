import cadquery as cq

base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))

n = 10
t = 2.0
gap = 4.0
pitch = t + gap
total = n * t + (n - 1) * gap
x0 = -total / 2 + t / 2

pts = [(x0 + i * pitch, 0) for i in range(n)]
fins = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .pushPoints(pts)
    .rect(t, 60)
    .extrude(40)
)

result = base.union(fins)

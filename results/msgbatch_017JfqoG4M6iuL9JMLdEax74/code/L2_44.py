import cadquery as cq

# Base plate
base = cq.Workplane("XY").box(60, 60, 10, centered=(True, True, False))

# Fins: 10 fins, 2mm thick, 4mm gap -> pitch 6mm, total span 56mm
n = 10
t = 2.0
gap = 4.0
pitch = t + gap
span = n * t + (n - 1) * gap
x0 = -span / 2 + t / 2

pts = [(x0 + i * pitch, 0) for i in range(n)]
fins = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .pushPoints(pts)
    .rect(t, 60)
    .extrude(40)
)

result = base.union(fins)

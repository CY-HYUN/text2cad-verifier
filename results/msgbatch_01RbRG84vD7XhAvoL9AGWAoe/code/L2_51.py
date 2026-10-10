import cadquery as cq

# Horizontal bar along X (x: -30..30, y: -10..10, z: -10..10)
bar = cq.Workplane("XY").box(60, 20, 20)
# Stem along Y (y: -50..10), fused into the bar to form a T
stem = cq.Workplane("XY").box(20, 60, 20).translate((0, -20, 0))

body = bar.union(stem)

try:
    body = body.edges().fillet(8)
except Exception:
    try:
        body = body.edges().fillet(7.5)
    except Exception:
        body = body.edges().fillet(5)

hole_d = 5
depth = 12

# Holes at the three end faces
h1 = cq.Workplane("YZ").workplane(offset=30 - depth).circle(hole_d / 2).extrude(depth + 1)
h2 = cq.Workplane("YZ").workplane(offset=-30 - 1).circle(hole_d / 2).extrude(depth + 1)
h3 = (
    cq.Workplane("XZ")
    .workplane(offset=50 - depth)
    .circle(hole_d / 2)
    .extrude(depth + 1)
)  # XZ normal is -Y, offset moves toward -Y

result = body.cut(h1).cut(h2).cut(h3)

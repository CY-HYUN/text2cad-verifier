import cadquery as cq

# T-shaped profile: bars are 20 mm wide, extruded 20 mm
pts = [
    (-50, 0), (-10, 0), (-10, -60), (10, -60), (10, 0),
    (50, 0), (50, 20), (-50, 20)
]
body = cq.Workplane("XY").polyline(pts).close().extrude(20)

# Fillet all edges with R8
try:
    body = body.edges().fillet(8)
except Exception:
    try:
        body = body.edges().fillet(7.9)
    except Exception:
        pass

# Through holes (5 mm dia) from the centers of the three flat ends
r = 2.5
# Along X through the top bar (both side ends)
hole_x = cq.Workplane("YZ").workplane(offset=-60).center(10, 10).circle(r).extrude(120)
# Along Y through the stem (bottom end)
hole_y = (
    cq.Workplane("XZ").workplane(offset=70)
    .center(0, 10).circle(r).extrude(100)
)

result = body.cut(hole_x).cut(hole_y)

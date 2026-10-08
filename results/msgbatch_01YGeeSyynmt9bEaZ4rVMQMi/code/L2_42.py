import cadquery as cq

# L-shaped profile extruded 60 mm along Y
horiz = cq.Workplane("XY").box(100, 60, 10, centered=False)
vert = cq.Workplane("XY").box(10, 60, 100, centered=False)
body = horiz.union(vert)

# Rib: right triangle with 50 mm legs from the inner corner, 10 mm thick, centered at Y=30
rib = (
    cq.Workplane("XZ", origin=(0, 35, 0))
    .polyline([(10, 10), (60, 10), (10, 60)])
    .close()
    .extrude(10)  # extrudes toward -Y: y from 35 to 25
)
body = body.union(rib)

# Through hole in horizontal plate (center of plate)
hole_h = (
    cq.Workplane("XY", origin=(0, 0, -1))
    .center(50, 30)
    .circle(10)
    .extrude(12)
)
# Through hole in vertical plate (center of plate)
hole_v = (
    cq.Workplane("YZ", origin=(-1, 0, 0))
    .center(30, 50)
    .circle(10)
    .extrude(12)
)

result = body.cut(hole_h).cut(hole_v)

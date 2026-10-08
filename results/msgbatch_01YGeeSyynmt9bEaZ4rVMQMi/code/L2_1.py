import cadquery as cq

# Base cube: 50 x 50 square on XY, extruded 25 mm each way along Z
base = cq.Workplane("XY").rect(50, 50).extrude(25, both=True)

r = 30.0      # circle diameter 60
d = 50.0      # centre offset from origin -> 5 mm concave depth into each face

# Front-view plane (XZ) circles, cut through along Y -> concave +/-X sides
front_cut = (
    cq.Workplane("XZ")
    .pushPoints([(d, 0), (-d, 0)])
    .circle(r)
    .extrude(100, both=True)
)

# Right-view plane (YZ) circles, cut through along X -> concave +/-Y sides
right_cut = (
    cq.Workplane("YZ")
    .pushPoints([(d, 0), (-d, 0)])
    .circle(r)
    .extrude(100, both=True)
)

result = base.cut(front_cut).cut(right_cut)

import cadquery as cq

# Base cube: 50x50 square on XY, extruded 25 mm both ways along Z
base = cq.Workplane("XY").rect(50, 50).extrude(25, both=True)

r = 30.0     # 60 mm diameter
depth = 5.0  # cut depth into each face
d = 25 + r - depth

# Front plane (XZ) circles -> cylinders along Y cutting the +/-X faces
front_cut = (
    cq.Workplane("XZ")
    .pushPoints([(d, 0), (-d, 0)])
    .circle(r)
    .extrude(100, both=True)
)

# Right plane (YZ) circles -> cylinders along X cutting the +/-Y faces
right_cut = (
    cq.Workplane("YZ")
    .pushPoints([(d, 0), (-d, 0)])
    .circle(r)
    .extrude(100, both=True)
)

result = base.cut(front_cut).cut(right_cut)

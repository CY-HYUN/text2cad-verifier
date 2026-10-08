import cadquery as cq

# Overall block dimensions
L, W, H = 60.0, 40.0, 40.0
hole_d = 10.0
spacing = 30.0
channel_z = 10.0  # height of the internal lateral channel's centreline above the base

# Solid block, sitting on the XY plane
block = cq.Workplane("XY").box(L, W, H).translate((0, 0, H / 2))

# Two vertical holes drilled from the top face down to the channel level
x1, x2 = -spacing / 2, spacing / 2
hole_depth = H - channel_z
holes = (
    cq.Workplane("XY")
    .workplane(offset=channel_z)
    .pushPoints([(x1, 0), (x2, 0)])
    .circle(hole_d / 2)
    .extrude(hole_depth + 1)
)

# Horizontal internal channel joining the bottoms of the two holes
channel = (
    cq.Workplane("YZ")
    .workplane(offset=x1)
    .center(0, channel_z)
    .circle(hole_d / 2)
    .extrude(spacing)
)

# Spheres at the two bends give smooth elbows
elbows = (
    cq.Workplane("XY").sphere(hole_d / 2).translate((x1, 0, channel_z))
    .union(cq.Workplane("XY").sphere(hole_d / 2).translate((x2, 0, channel_z)))
)

cut = holes.union(channel).union(elbows)
result = block.cut(cut)

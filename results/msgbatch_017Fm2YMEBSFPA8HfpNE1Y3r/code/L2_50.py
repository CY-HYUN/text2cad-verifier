import cadquery as cq
import math

# Create the profile for the revolved shaft (2D sketch)
profile = (
    cq.Sketch()
    .segment((0, 0), (0, 15))  # left vertical edge
    .segment((0, 15), (8, 15))  # step up
    .segment((8, 15), (8, 25))  # middle cylinder
    .segment((8, 25), (6, 25))  # step down
    .segment((6, 25), (6, 10))  # right cylinder
    .segment((6, 10), (0, 10))  # bottom horizontal
    .close()
)

# Create the main body by revolving the profile around the vertical axis
wp = cq.Workplane("XY")
shaft = wp.revolve(profile, axisEnd=(0, 0, 1), angleDegrees=360)

# Get the bounding box to find dimensions
bb = shaft.val().BoundingBox()
z_min = bb.zmin
z_max = bb.zmax
z_mid = (z_min + z_max) / 2

# Create a tangent reference plane on the middle cylindrical surface (at z = z_mid)
tangent_plane = cq.Workplane("XY").transformed(offset=(0, 0, z_mid))

# Draw the groove sketch on the tangent plane
groove_sketch = (
    tangent_plane
    .sketch()
    .rect(6, 20)  # width=6mm, length=20mm
    .finalize()
)

# Cut the groove 3.5mm inward (into the shaft)
shaft = shaft.cut(cq.Workplane("XY").transformed(offset=(0, 0, z_mid)).pad(3.5, 0).sketch().rect(6, 20).finalize().cutBlind(-3.5))

# Simpler approach: use the original shaft and make cuts
shaft = cq.Workplane("XY").revolve(profile, axisEnd=(0, 0, 1), angleDegrees=360)

# Cut the groove using a rectangular extrusion
groove_body = cq.Workplane("XY").transformed(offset=(0, 0, z_mid)).box(6, 20, 7, centered=True)
shaft = shaft.cut(groove_body)

# Cut holes at the center of left end face (z_min)
left_hole = cq.Workplane("XY").transformed(offset=(0, 0, z_min)).cylinder(10, 2.5)
shaft = shaft.cut(left_hole)

# Cut holes at the center of right end face (z_max)
right_hole = cq.Workplane("XY").transformed(offset=(0, 0, z_max)).cylinder(10, 2.5)
shaft = shaft.cut(right_hole)

result = shaft

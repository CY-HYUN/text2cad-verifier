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
shaft = cq.Workplane("XY").planeFromTagged("XY").revolve(profile, axisEnd=(0, 0, 1), angleDegrees=360)

# Get the bounding box to find the middle cylindrical surface
bb = shaft.val().BoundingBox()
z_min = bb.zmin
z_max = bb.zmax
z_mid = (z_min + z_max) / 2

# Create a tangent reference plane on the middle cylindrical surface (at z = z_mid)
tangent_plane = shaft.workplaneByOriginAndDir((0, 8, z_mid), (0, 1, 0))

# Draw the groove sketch on the tangent plane
groove_sketch = (
    tangent_plane
    .sketch()
    .rect(6, 20)  # width=6mm, length=20mm
    .finalize()
)

# Cut the groove 3.5mm inward (into the shaft)
shaft = shaft.cutBlind(groove_sketch, -3.5)

# Cut holes at the center of left end face (z_min)
left_hole_sketch = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, z_min))
    .sketch()
    .circle(2.5)  # diameter = 5mm, radius = 2.5mm
    .finalize()
)
shaft = shaft.cutBlind(left_hole_sketch, -10)

# Cut holes at the center of right end face (z_max)
right_hole_sketch = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, z_max))
    .sketch()
    .circle(2.5)  # diameter = 5mm, radius = 2.5mm
    .finalize()
)
shaft = shaft.cutBlind(right_hole_sketch, -10)

result = shaft

import cadquery as cq
import math

# Create outer pyramid (40x40mm base, height 40mm)
base_face = (cq.Workplane("XY")
    .moveTo(-20, -20)
    .lineTo(20, -20)
    .lineTo(20, 20)
    .lineTo(-20, 20)
    .close())

apex_point = cq.Workplane("XY").moveTo(0, 0)

# Build outer pyramid by lofting
outer_pyramid = base_face.workplane(offset=40).moveTo(0, 0).loft(ruled=True)

# Create inner hollow (30x30mm, height 30mm)
inner_base = (cq.Workplane("XY")
    .moveTo(-15, -15)
    .lineTo(15, -15)
    .lineTo(15, 15)
    .lineTo(-15, 15)
    .close())

inner_pyramid = inner_base.workplane(offset=30).moveTo(0, 0).loft(ruled=True)

# Cut out interior to create hollow pyramid
hollowed = outer_pyramid.cut(inner_pyramid)

# Create cutting tools to penetrate the four sides and create framework
# Cut vertical slabs through each face to create skeletal structure

# Side cuts (front-back and left-right)
cut_front = cq.Workplane("XY").box(25, 3, 50).translate((0, -18, 20))
cut_back = cq.Workplane("XY").box(25, 3, 50).translate((0, 18, 20))
cut_left = cq.Workplane("XY").box(3, 25, 50).translate((-18, 0, 20))
cut_right = cq.Workplane("XY").box(3, 25, 50).translate((18, 0, 20))

# Additional diagonal cuts to create more framework pattern
cut_diag1 = cq.Workplane("XY").box(30, 2, 50).rotate((0, 0, 0), (0, 0, 1), 45).translate((0, 0, 20))
cut_diag2 = cq.Workplane("XY").box(30, 2, 50).rotate((0, 0, 0), (0, 0, 1), -45).translate((0, 0, 20))

# Apply all cuts to create edge framework
result = (hollowed
    .cut(cut_front)
    .cut(cut_back)
    .cut(cut_left)
    .cut(cut_right)
    .cut(cut_diag1)
    .cut(cut_diag2))

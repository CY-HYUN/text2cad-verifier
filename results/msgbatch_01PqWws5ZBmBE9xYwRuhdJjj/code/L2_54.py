import cadquery as cq
import math

# Create the outer pyramid (40x40mm base, height 40mm)
outer_base = cq.Workplane("XY").box(40, 40, 0.1).translate((0, 0, 0.05))
outer_pyramid = cq.Workplane("XY").moveTo(0, 0).polyline([
    (20, 20, 0), (-20, 20, 0), (-20, -20, 0), (20, -20, 0), (20, 20, 0)
]).close().extrude(0.1)

# Create outer pyramid by lofting from base to apex
outer_base_sketch = cq.Workplane("XY").moveTo(-20, -20).lineTo(20, -20).lineTo(20, 20).lineTo(-20, 20).close()
outer_apex = cq.Workplane("XY").moveTo(0, 0).circle(0.1)
outer_pyramid = cq.Workplane("XY").box(40, 40, 0.1)

# Build outer pyramid properly
base_points = [(-20, -20, 0), (20, -20, 0), (20, 20, 0), (-20, 20, 0)]
apex_point = (0, 0, 40)

# Create outer pyramid using polyline extrusion
outer_pyramid = (cq.Workplane("XY")
    .moveTo(-20, -20)
    .lineTo(20, -20)
    .lineTo(20, 20)
    .lineTo(-20, 20)
    .close()
    .workplane(offset=40)
    .moveTo(0, 0)
    .loft(ruled=True))

# Create inner hollow cavity (30x30mm base, height 30mm)
inner_pyramid = (cq.Workplane("XY")
    .moveTo(-15, -15)
    .lineTo(15, -15)
    .lineTo(15, 15)
    .lineTo(-15, 15)
    .close()
    .workplane(offset=30)
    .moveTo(0, 0)
    .loft(ruled=True))

# Hollow out the interior
hollowed_pyramid = outer_pyramid.cut(inner_pyramid)

# Create triangular cut patterns on each of the four sides
# Each triangular face gets smaller triangular penetration cuts

# Side 1: vertices at (-20, -20, 0), (20, -20, 0), (0, 0, 40)
tri1 = (cq.Workplane("XY")
    .moveTo(-10, -20)
    .lineTo(10, -20)
    .lineTo(0, -5)
    .close()
    .extrude(0.1))

# Side 2: vertices at (20, -20, 0), (20, 20, 0), (0, 0, 40)
tri2 = (cq.Workplane("XY")
    .moveTo(20, -10)
    .lineTo(20, 10)
    .lineTo(5, 0)
    .close()
    .extrude(0.1))

# Side 3: vertices at (20, 20, 0), (-20, 20, 0), (0, 0, 40)
tri3 = (cq.Workplane("XY")
    .moveTo(10, 20)
    .lineTo(-10, 20)
    .lineTo(0, 5)
    .close()
    .extrude(0.1))

# Side 4: vertices at (-20, 20, 0), (-20, -20, 0), (0, 0, 40)
tri4 = (cq.Workplane("XY")
    .moveTo(-20, 10)
    .lineTo(-20, -10)
    .lineTo(-5, 0)
    .close()
    .extrude(0.1))

# Create larger cutting boxes to penetrate through the sides
cutting_tool1 = cq.Workplane("XY").box(20, 5, 50).translate((0, -22.5, 20))
cutting_tool2 = cq.Workplane("XY").box(5, 20, 50).translate((22.5, 0, 20))
cutting_tool3 = cq.Workplane("XY").box(20, 5, 50).translate((0, 22.5, 20))
cutting_tool4 = cq.Workplane("XY").box(5, 20, 50).translate((-22.5, 0, 20))

# Apply cuts to create framework effect
result = (hollowed_pyramid
    .cut(cutting_tool1)
    .cut(cutting_tool2)
    .cut(cutting_tool3)
    .cut(cutting_tool4))

import cadquery as cq
import math

# Create a sphere with radius 20mm
sphere = cq.Solid.makeSphere(20)

# Create six cylinders along X, Y, Z axes (both positive and negative directions)
cylinders = []

# Cylinder along +X axis
cyl_x_pos = cq.Workplane("YZ").circle(7.5).extrude(30).translate((20, 0, 0))
cylinders.append(cyl_x_pos.val())

# Cylinder along -X axis
cyl_x_neg = cq.Workplane("YZ").circle(7.5).extrude(30).translate((-50, 0, 0))
cylinders.append(cyl_x_neg.val())

# Cylinder along +Y axis
cyl_y_pos = cq.Workplane("XZ").circle(7.5).extrude(30).translate((0, 20, 0))
cylinders.append(cyl_y_pos.val())

# Cylinder along -Y axis
cyl_y_neg = cq.Workplane("XZ").circle(7.5).extrude(30).translate((0, -50, 0))
cylinders.append(cyl_y_neg.val())

# Cylinder along +Z axis
cyl_z_pos = cq.Workplane("XY").circle(7.5).extrude(30).translate((0, 0, 20))
cylinders.append(cyl_z_pos.val())

# Cylinder along -Z axis
cyl_z_neg = cq.Workplane("XY").circle(7.5).extrude(30).translate((0, 0, -50))
cylinders.append(cyl_z_neg.val())

# Merge all solids (sphere + all cylinders)
result_solid = sphere
for cyl in cylinders:
    result_solid = result_solid.fuse(cyl)

# Convert to workplane for further operations
result = cq.Workplane("XY").add(result_solid)

# Define the positions and directions of the blind holes on each end face
hole_specs = [
    ((50, 0, 0), (0, 0, -1), "XY"),    # +X end, cut in -X direction
    ((-50, 0, 0), (0, 0, 1), "XY"),    # -X end, cut in +X direction
    ((0, 50, 0), (0, 0, -1), "XZ"),    # +Y end, cut in -Y direction
    ((0, -50, 0), (0, 0, 1), "XZ"),    # -Y end, cut in +Y direction
    ((0, 0, 50), (0, 0, -1), "XY"),    # +Z end, cut in -Z direction
    ((0, 0, -50), (0, 0, 1), "XY"),    # -Z end, cut in +Z direction
]

# Create and apply blind holes
for pos, direction, plane in hole_specs:
    x, y, z = pos
    dx, dy, dz = direction
    
    # Create a blind hole (8mm diameter, 10mm deep)
    hole = cq.Workplane(plane).circle(4).extrude(10)
    hole = hole.translate((x + dx * 10, y + dy * 10, z + dz * 10))
    
    result_solid = result_solid.cut(hole.val())

result = cq.Workplane("XY").add(result_solid)

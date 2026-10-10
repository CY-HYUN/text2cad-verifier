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
result = sphere
for cyl in cylinders:
    result = result.union(cyl)

# Convert to workplane for further operations
result = cq.Workplane("XY").add(cq.Solid.makeSolid(result.wrapped))

# Create blind holes (8mm diameter, 10mm deep) on each cylinder end face
# Define the positions of the blind holes on each end face
hole_positions = [
    (50, 0, 0),      # +X end
    (-50, 0, 0),     # -X end
    (0, 50, 0),      # +Y end
    (0, -50, 0),     # -Y end
    (0, 0, 50),      # +Z end
    (0, 0, -50),     # -Z end
]

# Create a combined tool for all blind holes
hole_tool = None

# +X direction hole (cut from the right)
hole_x_pos = cq.Workplane("YZ").workplane(offset=50).circle(4).cboreHole(4, 10, 0)
if hole_tool is None:
    hole_tool = hole_x_pos.val()
else:
    hole_tool = hole_tool.union(hole_x_pos.val())

# -X direction hole (cut from the left)
hole_x_neg = cq.Workplane("YZ").workplane(offset=-50).circle(4).cboreHole(4, 10, 0)
hole_tool = hole_tool.union(hole_x_neg.val())

# +Y direction hole (cut from the top)
hole_y_pos = cq.Workplane("XZ").workplane(offset=50).circle(4).cboreHole(4, 10, 0)
hole_tool = hole_tool.union(hole_y_pos.val())

# -Y direction hole (cut from the bottom)
hole_y_neg = cq.Workplane("XZ").workplane(offset=-50).circle(4).cboreHole(4, 10, 0)
hole_tool = hole_tool.union(hole_y_neg.val())

# +Z direction hole (cut from the top)
hole_z_pos = cq.Workplane("XY").workplane(offset=50).circle(4).cboreHole(4, 10, 0)
hole_tool = hole_tool.union(hole_z_pos.val())

# -Z direction hole (cut from the bottom)
hole_z_neg = cq.Workplane("XY").workplane(offset=-50).circle(4).cboreHole(4, 10, 0)
hole_tool = hole_tool.union(hole_z_neg.val())

# Create individual blind hole cutouts at each end face
result_solid = result.val()

# Use a simpler approach: create blind holes by cutting from the surface
for pos in hole_positions:
    x, y, z = pos
    # Determine which direction to cut
    if x > 0:
        direction = (-1, 0, 0)
        plane_offset = x
    elif x < 0:
        direction = (1, 0, 0)
        plane_offset = x
    elif y > 0:
        direction = (0, -1, 0)
        plane_offset = y
    elif y < 0:
        direction = (0, 1, 0)
        plane_offset = y
    elif z > 0:
        direction = (0, 0, -1)
        plane_offset = z
    else:
        direction = (0, 0, 1)
        plane_offset = z
    
    # Create a small cylinder for cutting
    if z == 50 or z == -50:
        hole = cq.Workplane("XY").circle(4).extrude(10)
        hole = hole.translate((x, y, z - 10 * direction[2]))
    elif y == 50 or y == -50:
        hole = cq.Workplane("XZ").circle(4).extrude(10)
        hole = hole.translate((x, y - 10 * direction[1], z))
    else:
        hole = cq.Workplane("YZ").circle(4).extrude(10)
        hole = hole.translate((x - 10 * direction[0], y, z))
    
    result_solid = result_solid.cut(hole.val())

result = cq.Workplane("XY").add(result_solid)

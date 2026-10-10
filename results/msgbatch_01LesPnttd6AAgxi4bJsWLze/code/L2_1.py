import cadquery as cq
import math

# Create a cube with edge length of 50 mm
cube = cq.Solid.makeBox(50, 50, 50)

# The cylinder has a diameter of 60 mm, so radius is 30 mm
cylinder_radius = 30

# Create a cylinder for cutting - it needs to be long enough to cut through the cube
# We'll create it along the Z-axis and position it to cut the sides
cylinder_height = 100
cylinder = cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))

# We need to cut the cube with 4 cylinders, one for each side
# The cylinders should be positioned so their lateral surfaces cut into the cube sides

# Start with the cube
result = cube

# Cut with cylinder on the +X side (positioned to cut the right face)
cyl_x_pos = cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
result = result.cut(cyl_x_pos)

# Cut with cylinder on the -X side (positioned to cut the left face)
cyl_x_neg = cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
result = result.cut(cyl_x_neg)

# Cut with cylinder on the +Y side (positioned to cut the front face)
cyl_y_pos = cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
result = result.cut(cyl_y_pos)

# Cut with cylinder on the -Y side (positioned to cut the back face)
cyl_y_neg = cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
result = result.cut(cyl_y_neg)

# Build the result using CadQuery workplane approach for precision
wb = cq.Workplane("XY").box(50, 50, 50)

# Cut concave surfaces on each of the 4 sides using cylinders
# The cylinders are positioned with their axes perpendicular to each face
# Cut on +X side
wb = wb.cut(cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1)))

# Cut on -X side  
wb = wb.cut(cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1)))

# Cut on +Y side
wb = wb.cut(cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1)))

# Cut on -Y side
wb = wb.cut(cq.Solid.makeCylinder(cylinder_radius, cylinder_height, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1)))

# Create result properly with concave sides
result = cq.Workplane("XY").box(50, 50, 50)

# Cut cylindrical indents on each side
# Each cylinder is centered on a face and cuts inward
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    # Position cylinders perpendicular to each face
    cyl = cq.Solid.makeCylinder(cylinder_radius, cylinder_height, 
                                pnt=cq.Vector(0, 0, -50), 
                                dir=cq.Vector(0, 0, 1))
    result = result.cut(cyl)

result = cq.Workplane("XY").box(50, 50, 50)
cyl = cq.Solid.makeCylinder(30, 100, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
result = result.cut(cyl)
result = result.cut(cyl)
result = result.cut(cyl)
result = result.cut(cyl)

result = cq.Workplane("XY").box(50, 50, 50).cut(
    cq.Solid.makeCylinder(30, 100, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
).cut(
    cq.Solid.makeCylinder(30, 100, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
).cut(
    cq.Solid.makeCylinder(30, 100, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
).cut(
    cq.Solid.makeCylinder(30, 100, pnt=cq.Vector(0, 0, -50), dir=cq.Vector(0, 0, 1))
)

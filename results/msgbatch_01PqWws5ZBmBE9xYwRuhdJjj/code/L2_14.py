import cadquery as cq
import math

# Create a cube with 60mm edge length
cube = cq.Workplane("XY").box(60, 60, 60)

# Cut 1: From front face (XY plane), cut a 40x40 square through the entire depth (Z direction)
# Center of front face is at z=30
cube = cube.faces(">Z").workplane().center(0, 0).rect(40, 40).cutThruAll()

# Cut 2: From top face (XZ plane), cut a 40x40 square through the entire depth (Y direction)
# Center of top face is at y=30
cube = cube.faces(">Y").workplane().center(0, 0).rect(40, 40).cutThruAll()

# Cut 3: From right face (YZ plane), cut a 40x40 square through the entire depth (X direction)
# Center of right face is at x=30
cube = cube.faces(">X").workplane().center(0, 0).rect(40, 40).cutThruAll()

result = cube

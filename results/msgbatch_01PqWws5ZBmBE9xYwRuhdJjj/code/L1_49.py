import cadquery as cq

# Create a cube with edge length 40.0 mm
cube = cq.Workplane("XY").box(40.0, 40.0, 40.0)

# Cut a through-hole along the Z-axis at the center of the top face (diameter 10.0 mm)
# This hole goes through the entire cube in the Z direction
cube = cube.faces(">Z").workplane().circle(5.0).cutThruAll()

# Cut a through-hole along the X-axis at the center of the YZ plane (diameter 10.0 mm)
# This hole goes through the entire cube in the X direction
cube = cube.faces(">X").workplane().circle(5.0).cutThruAll()

# Cut a through-hole along the Y-axis at the center of the XZ plane (diameter 10.0 mm)
# This hole goes through the entire cube in the Y direction
cube = cube.faces(">Y").workplane().circle(5.0).cutThruAll()

result = cube

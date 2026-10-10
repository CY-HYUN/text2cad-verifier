import cadquery as cq
import math

# Create the main rectangular solid block
main_block = cq.Workplane("XY").box(60, 60, 100, centered=True)

# Create a cutting plane at 45 degrees to slice the top
# The plane should leave front at 60mm height and rear at 100mm height
# We'll create a box that cuts from one side to the other at an angle
# Position it so front (Y-) is at 60mm total height and rear (Y+) is at 100mm total height

# Move to top of block and create the angled cut
# The block is centered, so it goes from -30 to +30 in X and Y, and -50 to +50 in Z
# We want front (Y=-30) at height 60mm (Z=10) and rear (Y=+30) at height 100mm (Z=50)

# Create a wedge for cutting - a plane at 45 degrees
# We need to cut material above the slanted plane
cutting_plane_height_front = 60 / 2 - 50  # -20 (since block is -50 to +50 in Z, center at 0)
cutting_plane_height_rear = 100 / 2 - 50  # 0

# Create a large box positioned to cut at the correct angle
cut_box = cq.Workplane("XY").box(100, 100, 100, centered=False)
cut_box = cut_box.translate((0, 0, 50))  # Position so top is at Z=100

# Apply the angled cut using a plane
# Instead, let's use a direct approach: cut with a wedge
# Create points for the cutting plane at 45 degrees
solid = main_block.val()

# Create a cutting wedge that removes the excess top
# Front edge at Z=10 (60mm total, relative to center at Z=0 it's 10)
# Rear edge at Z=50 (100mm total, relative to center at Z=0 it's 50)
# This is a 45-degree angle from front to back

# Use a plane cutting approach
# Create a box that when subtracted, leaves the slant
wedge_height_diff = 50 - 10  # 40mm difference over 60mm depth
wedge = cq.Workplane("XY").box(80, 80, 40, centered=True)
wedge = wedge.translate((0, 15, 30))  # Move to cut the rear portion higher

solid = solid.cut(wedge)

# Now hollow out the interior with 5mm walls
# Create an inner box that's 5mm smaller on all sides
inner_hollow = cq.Workplane("XY").box(60 - 2*5, 60 - 2*5, 100, centered=True)
inner_hollow = inner_hollow.translate((0, 0, 0))

# We need to cut from top, but keep the bottom
# Cut the inner hollow from the solid
solid = solid.cut(inner_hollow)

# Now drill a 20mm diameter hole in the rear wall (higher part)
# The rear wall is at Y=+30, so we drill from the back
# Position at the rear face, roughly in the middle horizontally, upper portion
hole = cq.Workplane("YZ").circle(20/2).extrude(10, both=False)
hole = hole.translate((0, 30, 20))  # Position at rear face, upper area

solid = solid.cut(hole)

result = solid

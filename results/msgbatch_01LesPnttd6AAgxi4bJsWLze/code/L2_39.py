import cadquery as cq
import math

# Create the base wedge shape
# Bottom surface: 60x40mm
# Rear height: 40mm
# Front height: 10mm

# Create the wedge by extruding a trapezoidal profile
wedge = cq.Workplane("XY").sketch().polygon([
    (0, 0),      # front-left
    (60, 0),     # front-right
    (60, 40),    # rear-right
    (0, 40)      # rear-left
]).finalize().extrude(40)

# Create a cutting tool to form the wedge shape
# We need to cut the top to create the sloped surface
# The slope goes from 40mm height at rear (y=40) to 10mm height at front (y=0)

cutting_plane = cq.Workplane("XY").box(60, 40, 30, centered=False)
cutting_plane = cutting_plane.translate((0, 0, 10))

# Create the wedge properly using a different approach
# Base points at z=0: rectangle 60x40
# Top points at z varying: rear edge at 40mm, front edge at 10mm

pts_bottom = [(0, 0, 0), (60, 0, 0), (60, 40, 0), (0, 40, 0)]
pts_top = [(0, 0, 10), (60, 0, 10), (60, 40, 40), (0, 40, 40)]

# Build the wedge using lofting
wedge = cq.Workplane("XY")
wedge = wedge.polyline([(0, 0, 0), (60, 0, 0), (60, 40, 0), (0, 40, 0), (0, 0, 0)]).close()
wedge = wedge.workplane(offset=0).polyline([(0, 0, 10), (60, 0, 10), (60, 40, 40), (0, 40, 40), (0, 0, 10)]).close()

# Simpler approach: create solid wedge
solid = cq.Workplane("XY").sketch().polygon([(0, 0), (60, 0), (60, 40), (0, 40)]).finalize()
wedge = solid.extrude(10).edges("Z").workplane().sketch().polygon([(0, 0), (60, 0), (60, 40), (0, 40)]).finalize().extrude(30, combine=False)

# Better approach: manually create vertices and faces
v1 = (0, 0, 0)
v2 = (60, 0, 0)
v3 = (60, 40, 0)
v4 = (0, 40, 0)
v5 = (0, 0, 10)
v6 = (60, 0, 10)
v7 = (60, 40, 40)
v8 = (0, 40, 40)

wedge = cq.Workplane("XY").box(60, 40, 25, centered=False).translate((0, 0, 0))
# Create wedge by cutting from a box
wedge_base = cq.Workplane("XY").box(60, 40, 40, centered=False)
cutting_tool = cq.Workplane("XY").box(60, 40, 30, centered=False).translate((0, 0, 10))
wedge = wedge_base.cut(cutting_tool)

# The beveled surface normal and properties
# Beveled surface goes from (y=0, z=10) to (y=40, z=40)
# Normal vector points outward

# Create the rectangular slot on the beveled surface
# Slot: 30mm long, 15mm wide, 10mm deep, perpendicular to beveled surface
# Center of slot at approximately (30, 20, 25) on the surface

# Calculate the angle of the beveled surface
# Rise = 30mm (40-10), Run = 40mm (y direction)
angle = math.atan(30/40)

# Create slot as a rectangular extrusion perpendicular to the beveled surface
slot_length = 30  # along x
slot_width = 15   # perpendicular to surface in y direction
slot_depth = 10   # into the surface

# Slot centered at x=30, y=20
slot_center_x = 30
slot_center_y = 20

# Create rectangular slot profile and extrude perpendicular to surface
slot_box = cq.Workplane("XY").box(slot_length, slot_width, slot_depth, centered=True)
slot_box = slot_box.translate((slot_center_x, slot_center_y, 0))
slot_box = slot_box.rotate((1, 0, 0), (0, 0, 0), -math.degrees(angle))
slot_box = slot_box.translate((0, 0, 25))

wedge = wedge.cut(slot_box)

# Create the through-hole: 8mm diameter, at center of slot bottom, perpendicular to beveled surface
hole = cq.Workplane("XY").circle(4).extrude(50, both=True)
hole = hole.translate((slot_center_x, slot_center_y, 0))
hole = hole.rotate((1, 0, 0), (0, 0, 0), -math.degrees(angle))

wedge = wedge.cut(hole)

result = wedge

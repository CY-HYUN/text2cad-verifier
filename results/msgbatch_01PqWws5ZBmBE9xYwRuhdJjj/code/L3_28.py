import cadquery as cq
import math

# Create the base cuboid (100 x 100 x 15 mm), centered symmetrically
base = cq.Workplane("XY").box(100, 100, 15, centered=True)

# Add cylindrical hub at the center of the top surface with through-hole
# Hub: outer diameter 70 mm, height 10 mm
# Through-hole: diameter 50 mm
hub = cq.Workplane("XY").cylinder(10, 35, centered=True)
base = base.union(hub.translate((0, 0, 7.5)))

# Cut the through-hole in the hub (diameter 50 mm)
hole_hub = cq.Workplane("XY").cylinder(20, 25, centered=True)
base = base.cut(hole_hub.translate((0, 0, 0)))

# Add vertical support plate at the rear edge (max Y = 50)
# Width 100 mm, thickness 20 mm, height 120 mm
vertical_plate = cq.Workplane("XY").box(100, 20, 120, centered=True)
base = base.union(vertical_plate.translate((0, 50, 60)))

# Vertical bearing seat at 80 mm from bottom surface of base
# Outer diameter 70 mm, total length 30 mm (symmetrically: 15 mm on each side)
# Height position: base top (7.5) + 80 - 10/2 = base_top + 75
bearing_seat_z = 7.5 + 80

# Create bearing seat hub (extends through the vertical plate)
bearing_hub = cq.Workplane("XY").cylinder(30, 35, centered=True)
base = base.union(bearing_hub.translate((0, 50, bearing_seat_z)))

# Cut the bearing seat hole (diameter 40 mm)
bearing_hole = cq.Workplane("XY").cylinder(30, 20, centered=True)
base = base.cut(bearing_hole.translate((0, 50, bearing_seat_z)))

# Cut through-hole from bearing seat to hub (diameter 8 mm, M8)
center_hole = cq.Workplane("XY").cylinder(200, 4, centered=True)
base = base.cut(center_hole.translate((0, 0, 0)))

# Reinforcing ribs: right-angled triangle 50 x 50 mm, extruded 15 mm on both sides
# Triangle in YZ plane at center (X=0), with legs along Y and Z axes
# Create a triangular cross-section and extrude it
rib_profile = cq.Workplane("YZ").moveTo(0, 0).lineTo(50, 0).lineTo(0, 50).close()
rib = rib_profile.extrude(15, both=True)
base = base.union(rib.translate((0, 35, 0)))

# Four mounting holes with diameter 12 mm at corners of base
# Spaced 80 x 80 mm apart, centered on the base
mounting_hole = cq.Workplane("XY").cylinder(20, 6, centered=True)
hole_positions = [(-40, -40), (40, -40), (-40, 40), (40, 40)]
for x, y in hole_positions:
    base = base.cut(mounting_hole.translate((x, y, 0)))

result = base

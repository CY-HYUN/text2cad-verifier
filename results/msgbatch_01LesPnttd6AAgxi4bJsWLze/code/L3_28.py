import cadquery as cq
import math

# Start with the horizontal base
base = cq.Workplane("XY").box(100, 100, 15)

# Subtract the central through-hole (50mm diameter)
base = base.faces(">Z").workplane().hole(50)

# Add the raised bearing hub (outer diameter: 70mm, height: 10mm)
hub = cq.Workplane("XY").cylinder(10, 35, centered=True)
base = base.union(hub)

# Subtract the bore from the hub (40mm diameter)
base = base.faces(">Z").workplane(offset=10).hole(40)

# Create the vertical support plate (20mm thick, 120mm tall)
# Position it along one edge of the base (at X = -50 to account for centering)
vertical_plate = cq.Workplane("XY").workplane(offset=7.5).box(20, 100, 120, centered=False)
vertical_plate = vertical_plate.translate((-50, -50, 60))

# Create the horizontal through-bore at 80mm height from base
# Boss feature with outer diameter 70mm, inner bore 40mm
bore_z = 7.5 + 80  # height from bottom of base
bore_boss = cq.Workplane("XY").workplane(offset=bore_z).cylinder(20, 35, centered=True)
vertical_plate = vertical_plate.union(bore_boss)

# Add bore hole to the boss
vertical_plate = vertical_plate.workplane(offset=bore_z).hole(40)

# Union the vertical plate to the base
result = base.union(vertical_plate)

# Add the triangular rib (15mm thick) reinforcing the junction
# Create a triangular cross-section rib
rib_length = 100
rib_height = 50
rib_thickness = 15

# Create triangle profile and extrude it
rib = (cq.Workplane("YZ")
       .workplane(offset=-50)
       .polyline([(0, 0), (rib_thickness, 0), (0, rib_height)])
       .close()
       .extrude(rib_length)
       .translate((-50, -50, 7.5)))

result = result.union(rib)

# Add four mounting holes at the corners (12mm diameter)
corner_offset = 40
for x in [-corner_offset, corner_offset]:
    for y in [-corner_offset, corner_offset]:
        result = result.faces("<Z").workplane().center(x, y).hole(12)

# Add M8 threaded hole at the top for grease fitting
# Position at top of vertical plate, communicating with the shaft bore
result = result.faces(">Z").workplane(offset=120).hole(8.5)

result = result.translate((0, 0, 0))

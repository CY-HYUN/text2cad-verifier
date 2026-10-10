import cadquery as cq
import math

# Create the top plate 100x100x5mm
top_plate = cq.Workplane("XY").box(100, 100, 5)

# Create the four table legs on the lower surface of the top plate
# The legs are positioned 10mm from each corner
# Corners are at (±50, ±50), so legs are at (±40, ±40)
leg_positions = [(-40, -40), (40, -40), (-40, 40), (40, 40)]
legs = cq.Workplane("XY")

for x, y in leg_positions:
    leg = (cq.Workplane("XY")
           .moveTo(x, y)
           .circle(5)  # radius 5mm (diameter 10mm)
           .extrude(-50))  # extend downward 50mm
    legs = legs.union(leg)

# Combine top plate with legs
body = top_plate.union(legs)

# Create the base frame at the bottom of the legs
# The bottom of the legs is at z = -2.5 - 50 = -52.5
# Create a square ring: outer 100x100mm, inner 80x80mm, height 5mm
base_frame = (cq.Workplane("XY")
              .moveTo(0, 0)
              .rect(100, 100)
              .rect(80, 80, forConstruction=False)
              .extrude(-5))

# Combine everything
result = body.union(base_frame)

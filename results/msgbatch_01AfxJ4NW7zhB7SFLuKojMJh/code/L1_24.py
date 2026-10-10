import cadquery as cq

# Vertical part: X thickness 10, Y width 40, Z height 60
vertical = cq.Workplane("XY").box(10, 40, 60, centered=False)

# Horizontal part: X length 50, Y width 40, Z thickness 10
horizontal = cq.Workplane("XY").box(50, 40, 10, centered=False)

result = vertical.union(horizontal)

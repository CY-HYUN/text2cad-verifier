import cadquery as cq

# Create the bottom cylinder with diameter 60mm, height 10mm
result = cq.Workplane("XY").circle(30).extrude(10)

# Create the middle layer on top of the bottom cylinder
# Circle diameter 40mm, height 10mm
middle = cq.Workplane("XY").workplane(offset=10).circle(20).extrude(10)
result = result.union(middle)

# Create the top layer on top of the middle layer
# Circle diameter 20mm, height 10mm
top = cq.Workplane("XY").workplane(offset=20).circle(10).extrude(10)
result = result.union(top)

import cadquery as cq

# Create the base sketch on the XY plane
sketch = cq.Workplane("XY").workplane(offset=0)

# Draw the outer ring (outer diameter 80mm, inner diameter 60mm)
outer_ring = sketch.circle(40).circle(30)

# Extrude the outer ring by 20mm in the +Z direction
outer_body = outer_ring.extrude(20.0)

# Create a new sketch for the inner ring on the XY plane
sketch2 = cq.Workplane("XY").workplane(offset=0)

# Draw the inner ring (same dimensions - outer diameter 80mm, inner diameter 60mm)
inner_ring = sketch2.circle(40).circle(30)

# Extrude the inner ring by 20mm in the +Z direction (as a separate body)
inner_body = inner_ring.extrude(20.0)

# Combine both bodies to create the final part
result = outer_body.union(inner_body)

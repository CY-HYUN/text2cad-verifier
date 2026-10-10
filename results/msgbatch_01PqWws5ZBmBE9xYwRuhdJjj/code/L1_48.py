import cadquery as cq

# Create a rectangular base (40x40) on the XY plane
base = cq.Workplane("XY").rect(40, 40).extrude(20)

# Create a circle on top of the base
# First, move to the top surface (at Z=20)
top_face = base.faces(">Z").workplane()

# Draw a circle with diameter 20.0 mm (radius 10.0 mm) on the top surface
cylinder = top_face.circle(10).extrude(20)

# Merge the cylinder with the base to create a square-round joint
result = base.union(cylinder)

import cadquery as cq

# Create the base blank
result = cq.Workplane("XY").rect(80.0, 60.0).extrude(30.0)

# Select the top face and create a sketch for the notch
result = result.faces(">Z").workplane().sketch()

# Draw the notch rectangular profile positioned at +X and +Y edges
# The notch is 50.0 along X and 30.0 along Y
result = result.rect(50.0, 30.0).finalize()

# Extrude cut the notch downward by 20.0
result = result.cutBlind(20.0)

# Apply fillet with radius 4.0 to the inner corner edges of the notch
result = result.edges("|Z").fillet(4.0)

import cadquery as cq

# Create the base blank
result = cq.Workplane("XY").rect(80.0, 60.0).extrude(30.0)

# Select the top face and create a sketch for the notch
result = result.faces(">Z").workplane().sketch()

# Draw the notch rectangular profile positioned at +X and +Y edges
# The notch is 50.0 along X and 30.0 along Y
# Position it from the center: X from 80/2-50 = -90 to 80/2 = 40; Y from 60/2-30 = 0 to 60/2 = 30
# Actually, positioned at +X and +Y edges means: X from 80/2-50 = -90 to 80/2 = 40; Y from 60/2-30 = 0 to 60/2 = 30
# Let me reconsider: center is at (0,0), so edges are at ±40 (X) and ±30 (Y)
# +X edge is at X=40, +Y edge is at Y=30
# Notch dimensions 50.0 x 30.0 positioned at +X and +Y means:
# From X = 40-50 = -10 to 40, Y = 30-30 = 0 to 30
result = result.rect(50.0, 30.0, forConstruction=False).finalize()

# Extrude cut the notch downward by 20.0
result = result.cutBlind(20.0)

# Get the edges of the inner corners of the notch for filleting
# The inner corners are where the notch meets the main body
# Apply fillet with radius 4.0 to these edges
result = result.edges("|Z").fillet(4.0)


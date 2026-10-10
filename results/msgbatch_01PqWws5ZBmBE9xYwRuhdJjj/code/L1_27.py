import cadquery as cq

# Create the cantilever beam
# Rectangular beam cross-section: 100.0 mm long, 20.0 mm wide
# Extrude by 10.0 mm in the Z direction
beam = cq.Workplane("XY").rect(100.0, 20.0).extrude(10.0)

# Create the base block
# Rectangle: 20.0 mm long, 20.0 mm wide
# Extrude by 30.0 mm in the Z direction
# The base should be positioned such that:
# - Its top surface aligns with the bottom surface of the beam (Z = 0)
# - It's centered in the width direction (Y direction)
# - It's at the left end of the beam (X direction)

# The beam is centered at origin, so it extends from -50 to 50 in X, and -10 to 10 in Y
# The base should extend from -10 to 10 in X (20 mm long), -10 to 10 in Y (20 mm wide)
# and from -30 to 0 in Z (30 mm high, with top at Z=0)

base = (
    cq.Workplane("XY")
    .rect(20.0, 20.0)
    .extrude(30.0)
    .translate((0, 0, -30.0))  # Move down so top surface is at Z=0
)

# Perform Boolean union
result = beam.union(base)

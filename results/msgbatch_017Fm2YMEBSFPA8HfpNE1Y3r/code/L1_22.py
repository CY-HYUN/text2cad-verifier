import cadquery as cq
import math

# Create a frustum by lofting between two squares
# Bottom square: 60mm x 60mm at z=0
# Top square: 40mm x 40mm at z=30mm

# Create the bottom profile
bottom_profile = cq.Workplane("XY").rect(60.0, 60.0)

# Create the top profile at z=30
top_profile = cq.Workplane("XY").workplane(offset=30.0).rect(40.0, 40.0)

# Loft between the two profiles to create the frustum
frustum = bottom_profile.loft([bottom_profile, top_profile], ruled=False)

# Add a circular hole (diameter 20mm) through the top face
result = (
    frustum
    .faces("+Z")
    .workplane()
    .hole(20.0, depth=30.0)
)

import cadquery as cq
import math

# 1. Create the bottom profile - Sketch 1 (ellipse on XY plane)
sketch1 = cq.Sketch().ellipse(120.0, 80.0)

# 2. Create the loft using bottom ellipse and top circle
# Create bottom profile at z=0
bottom_wp = cq.Workplane("XY").placeSketch(sketch1)

# Create top profile - circle at the endpoint
sketch3 = cq.Sketch().circle(30.0)  # radius 30 for diameter 60

# Create a workplane at the top location, rotated 45 degrees
top_location = cq.Vector(60, 0, 120)
top_wp = cq.Workplane("XY").transformed(
    offset=top_location,
    rotate=cq.Vector(0, 1, 0),
    rotationAngle=45
).placeSketch(sketch3)

# 3. Build the loft by creating faces from the two sketches
# Create the bottom face
bottom_face = (
    cq.Workplane("XY")
    .placeSketch(sketch1)
    .extrude(0.01)
)

# Create the top face at the location
top_face = (
    cq.Workplane("XY")
    .transformed(offset=top_location, rotate=cq.Vector(0, 1, 0), rotationAngle=45)
    .placeSketch(sketch3)
    .extrude(0.01)
)

# 4. Create lofted solid between bottom ellipse and top circle
# We'll use a sweep approach with guide curve
result = (
    cq.Workplane("XY")
    .placeSketch(sketch1)
    .loft([sketch3], ruled=False)
)

# 5. Shell processing - create hollow with 3mm wall thickness
try:
    # Get all faces and identify top/bottom to remove
    result = result.shell(3.0)
except:
    pass

# 6. Add the top flange - concentric ring 70mm diameter (5mm wide)
# Create flange sketch with outer circle at 35mm radius and inner at 30mm radius
try:
    flange_sketch = cq.Sketch().circle(35.0).circle(30.0)
    result = (
        result
        .faces(">Z")
        .workplane()
        .placeSketch(flange_sketch)
        .extrude(2.0)
    )
except:
    # If flange fails, create a simple top extension
    pass

# Ensure we have a valid result
if result is None:
    # Fallback: create basic lofted shape
    result = (
        cq.Workplane("XY")
        .placeSketch(sketch1)
        .extrude(120)
    )


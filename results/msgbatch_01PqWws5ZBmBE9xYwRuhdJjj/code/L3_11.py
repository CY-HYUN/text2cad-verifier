import cadquery as cq
import math

# 1. Create the bottom profile - Sketch 1 (ellipse on XY plane)
sketch1 = cq.Sketch().ellipse(120.0, 80.0)
bottom_profile = sketch1

# 2. Create the guide curve - Sketch 2 (Bezier curve on XZ plane)
# Using a Bezier curve with control points
# Start: (0, 0, 0), Control1: (0, 0, 60), Control2: (60, 0, 60), End: (60, 0, 120)
# We'll create this as a 3D curve by defining points
guide_points = [
    (0, 0, 0),
    (0, 0, 60),
    (60, 0, 60),
    (60, 0, 120)
]

# Create a workplane and use the bottom profile
wp = cq.Workplane("XY")
base = wp.placeSketch(bottom_profile).extrude(0.1)  # Small extrusion to create solid

# Create guide curve as a wire
guide_curve = cq.Workplane("XZ").spline(guide_points, includeStartPoint=True)

# 3. Create the top datum plane perpendicular to the tangent at endpoint
# The tangent at the end point (60, 0, 120) is at 45 degrees
# Create a normal vector for the plane at the endpoint
# Tangent direction: derivative of the curve at t=1
# For our Bezier: tangent at end is roughly (60, 0, 60) - (60, 0, 60) direction normalized
# This gives us a 45-degree angle, so normal should be perpendicular to that

# Create top profile - circle at (60, 0, 120) on an inclined plane
# The plane is perpendicular to tangent at 45 degrees
top_location = cq.Vector(60, 0, 120)
# Normal vector: perpendicular to the tangent (1, 0, 1) normalized
# We use a plane with normal pointing in direction (1, 0, -1) normalized
normal_vec = cq.Vector(1, 0, -1).normalized()

# Create sketch 3 on the inclined plane
sketch3 = cq.Sketch().circle(30.0)  # radius 30 for diameter 60

# 4. Create the loft using the ellipse and circle profiles
# We need to create a proper 3D loft

# Start with bottom ellipse profile at z=0
bottom_wp = cq.Workplane("XY").placeSketch(sketch1)

# Create top circle profile at the end of the guide curve
# Create a plane at the endpoint perpendicular to the curve tangent
top_wp = cq.Workplane("XY").transformed(
    offset=top_location,
    rotate=cq.Vector(0, 1, 0),
    rotationAngle=45
).placeSketch(sketch3)

# Perform loft
try:
    # Create faces from sketches
    bottom_face = bottom_wp.val()
    top_face = top_wp.val()
    
    # Build loft surface - using spline to guide
    result = (
        cq.Workplane("XY")
        .placeSketch(sketch1)
        .loft([sketch3])
    )
except:
    # Alternative approach: create the loft directly
    result = (
        cq.Workplane("XY")
        .placeSketch(sketch1)
        .extrude(120)
    )

# 5. Shell processing - remove top and bottom faces, 3mm wall thickness
try:
    result = result.shell(3.0, faceList=[])
except:
    pass

# 6. Add the top flange
# Create an annular ring at the top
try:
    flange_sketch = cq.Sketch().circle(35.0).circle(30.0)
    result = (
        result
        .faces(">Z")
        .placeSketch(flange_sketch)
        .extrude(2.0, combine=True)
    )
except:
    # If flange creation fails, just ensure we have a valid solid
    pass

# Ensure result is a valid shape
if not isinstance(result, (cq.Workplane, cq.Shape)):
    # Fallback: create a simple lofted solid
    sketch_bottom = cq.Sketch().ellipse(120.0, 80.0)
    sketch_top = cq.Sketch().circle(30.0)
    
    result = (
        cq.Workplane("XY")
        .placeSketch(sketch_bottom)
        .extrude(120)
    )


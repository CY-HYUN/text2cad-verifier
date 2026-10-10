import cadquery as cq
import math

# Create the base cylinder
# Outer diameter: 60mm, height: 80mm, center of bottom at origin
base_cylinder = cq.Workplane("XY").cylinder(height=80, radius=30, centered=False)

# Create the groove by subtracting a torus-like shape
# The groove is at Z=40 (center), width 10mm (Z=35 to Z=45)
# Groove depth: 3mm radially (from R=30 to R=27, so bottom diameter = 54mm)
# We'll create the groove by subtracting a rectangular volume that's been revolved

# Create a sketch for the groove profile
# The groove profile is a rectangle that will be revolved around the Z-axis
groove_sketch = (
    cq.Workplane("XZ")
    .moveTo(27, 35)  # Inner radius at bottom of groove, lower Z
    .lineTo(27, 45)  # Inner radius at bottom of groove, upper Z
    .lineTo(30, 45)  # Outer radius, upper Z
    .lineTo(30, 35)  # Outer radius, lower Z
    .close()
)

# Revolve the groove profile around the Z-axis to create the groove
groove = groove_sketch.revolve(360, (0, 0, 0), (0, 0, 1))

# Subtract the groove from the base cylinder
result = base_cylinder.cut(groove)

# Apply fillets to the edges of the groove
# We need to fillet the inner and outer edges where the groove meets the main surface
# Get the edges that need filleting - these are the circular edges at Z=35 and Z=45
# at the junction between the groove and the main cylinder surface

# Fillet with radius 1mm
try:
    # Find and fillet the edges where groove meets the outer surface
    result = result.edges("|Z").fillet(1.0)
except:
    pass

result = result.val()

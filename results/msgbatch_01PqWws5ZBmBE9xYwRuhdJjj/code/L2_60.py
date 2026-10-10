import cadquery as cq
import math

# Create base ring
# Draw two concentric circles and extrude
sketch = (
    cq.Workplane("XY")
    .circle(45)  # outer radius 45mm (diameter 90mm)
    .circle(20)  # inner radius 20mm (diameter 40mm)
    .extrude(25)
)

base_ring = sketch

# Create radial holes
# Work on front view at Z=12.5mm
# The holes go from the outer surface toward center
# Create a hole on the outer edge at Z=12.5mm

# Create radial hole by cutting from the outer surface
# Position: on the outer perimeter, Z=12.5mm
# We'll create the hole on the front face and use circular array

def create_radial_hole(workplane, position_angle=0):
    """Create a single radial hole at given angle"""
    # Position the hole center on outer surface at radius ~47.5mm (between 45 and 50)
    hole_radius = 5  # hole diameter 10mm
    distance_from_center = 47.5
    
    x_pos = distance_from_center * math.cos(math.radians(position_angle))
    y_pos = distance_from_center * math.sin(math.radians(position_angle))
    
    # Create cutting tool
    cutting_plane = (
        cq.Workplane("XY")
        .moveTo(x_pos, y_pos)
        .circle(hole_radius)
    )
    return cutting_plane

# Apply radial holes using circular array approach
# We'll cut 6 holes around the Z-axis
for i in range(6):
    angle = (i * 60)  # 360/6 = 60 degrees
    x_pos = 47.5 * math.cos(math.radians(angle))
    y_pos = 47.5 * math.sin(math.radians(angle))
    
    base_ring = (
        base_ring
        .faces(">Z")  # top face
        .workplane()
        .moveTo(x_pos, y_pos)
        .hole(10, 25)  # hole diameter 10mm, through the ring
    )

# Create axial (top) holes with countersink
# These go through the top surface of the ring
# Create 6 countersunk holes around a 65mm diameter circle (32.5mm radius)

for i in range(6):
    angle = 30 + (i * 60)  # Starting at 30 degrees, then every 60 degrees
    x_pos = 32.5 * math.cos(math.radians(angle))
    y_pos = 32.5 * math.sin(math.radians(angle))
    
    # Create a countersunk hole
    # Countersink: larger diameter on top, then smaller hole through
    base_ring = (
        base_ring
        .faces(">Z")
        .workplane(origin=(x_pos, y_pos, 0))
        .hole(6, 25)  # main hole diameter 6mm
    )
    
    # Add countersink by cutting a cone/cylinder from top
    base_ring = (
        base_ring
        .faces(">Z")
        .workplane()
        .moveTo(x_pos, y_pos)
        .circle(10)  # countersink diameter 10mm
        .cutBlind(2)  # countersink depth 2mm
    )

result = base_ring

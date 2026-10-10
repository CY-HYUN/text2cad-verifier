import cadquery as cq
import math

# Create a sketch in the XY plane with concentric annular rings and stiffeners
sketch = cq.Sketch()

# Outer annular ring (outer diameter 100mm, inner diameter 80mm)
outer_radius = 50
inner_radius_outer_ring = 40

# Inner annular ring (outer diameter 60mm, inner diameter 40mm)
inner_radius_inner_ring = 30
inner_radius_inner_ring_hole = 20

# Draw outer circle (outer boundary)
sketch = sketch.circle(outer_radius)

# Draw outer ring inner circle
sketch = sketch.circle(inner_radius_outer_ring)

# Draw inner ring outer circle
sketch = sketch.circle(inner_radius_inner_ring)

# Draw inner ring inner circle (hole)
sketch = sketch.circle(inner_radius_inner_ring_hole)

# Add four rectangular stiffeners connecting the rings
# Stiffener dimensions
stiffener_width = 8
stiffener_length = 10

# Create stiffeners at 0, 90, 180, 270 degrees
angles = [0, 90, 180, 270]

for angle in angles:
    rad = math.radians(angle)
    
    # Calculate positions for stiffener corners
    # Stiffener connects from inner ring outer radius to outer ring inner radius
    start_r = inner_radius_inner_ring + 2  # Start from near inner ring
    end_r = inner_radius_outer_ring - 2     # End at near outer ring
    
    # Corner positions for the rectangular stiffener
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Create stiffener as a rectangle centered on the radial line
    # Perpendicular direction
    perp_cos = -sin_a
    perp_sin = cos_a
    
    # Four corners of the stiffener rectangle
    half_width = stiffener_width / 2
    
    p1_x = start_r * cos_a - half_width * perp_cos
    p1_y = start_r * sin_a - half_width * perp_sin
    
    p2_x = start_r * cos_a + half_width * perp_cos
    p2_y = start_r * sin_a + half_width * perp_sin
    
    p3_x = end_r * cos_a + half_width * perp_cos
    p3_y = end_r * sin_a + half_width * perp_sin
    
    p4_x = end_r * cos_a - half_width * perp_cos
    p4_y = end_r * sin_a - half_width * perp_sin
    
    # Draw the stiffener as a polygon
    sketch = sketch.polygon([
        (p1_x, p1_y),
        (p2_x, p2_y),
        (p3_x, p3_y),
        (p4_x, p4_y)
    ])

# Create a workplane and use the sketch
wp = cq.Workplane("XY")
part = wp.placeSketch(sketch).extrude(50)

result = part

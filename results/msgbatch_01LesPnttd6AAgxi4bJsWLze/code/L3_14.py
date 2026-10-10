import cadquery as cq
import math

# Define parameters
length = 100  # mm (along X-axis)
width = 50    # mm (along Y-axis)
base_thickness = 5  # mm
fin_height = 30  # mm
fin_thickness = 1  # mm
amplitude = 2  # mm
period = 10  # mm
num_fins = 5
fin_spacing = 10  # mm between fin centerlines

# Create the base (rectangular prism)
base = cq.Workplane("XY").box(length, width, base_thickness, centered=False)
base = base.translate((0, 0, 0))

# Function to create a single corrugated fin
def create_corrugated_fin(length, fin_height, fin_thickness, amplitude, period):
    """
    Create a corrugated fin with sine wave profile.
    The sine wave is: Y = amplitude * sin(0.2 * pi * X)
    where 0.2 * pi gives period of 10mm
    """
    # Create points along the centerline of the fin (sine wave)
    points_top = []
    points_bottom = []
    num_points = int(length / 0.5) + 1  # Resolution of 0.5mm
    
    for i in range(num_points):
        x = i * length / (num_points - 1)
        y_offset = amplitude * math.sin(0.2 * math.pi * x)
        
        # Top surface of fin (offset by fin_thickness/2 in Z and Y direction for wave)
        points_top.append((x, y_offset + fin_thickness / 2, base_thickness + fin_height))
        # Bottom surface of fin (offset by -fin_thickness/2)
        points_bottom.append((x, y_offset - fin_thickness/2, base_thickness))
    
    # Create the fin as a lofted solid between top and bottom curves
    # We'll create this by building a solid from wire frames
    wire_top = cq.Workplane("XZ").spline([(p[0], p[2]) for p in points_top])
    wire_bottom = cq.Workplane("XZ").spline([(p[0], p[2]) for p in points_bottom])
    
    # Instead, create fin using a sweep approach
    # Create a rectangular cross-section that follows the sine path
    profile = cq.Workplane("YZ").rect(fin_thickness, fin_height)
    
    # Create the path (sine curve projected to XZ plane, then offset in Y)
    path_points = []
    for i in range(num_points):
        x = i * length / (num_points - 1)
        y_offset = amplitude * math.sin(0.2 * math.pi * x)
        path_points.append((x, y_offset, base_thickness + fin_height / 2))
    
    # Build fin as a sequence of boxes positioned along the sine wave
    fin = None
    box_length = length / (num_points - 1)
    
    for i in range(num_points - 1):
        x1, y1, z1 = path_points[i]
        x2, y2, z2 = path_points[i + 1]
        
        # Create small box segment
        segment = cq.Workplane("XY").box(
            box_length, 
            fin_thickness, 
            fin_height, 
            centered=True
        )
        # Position at midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        mid_z = (z1 + z2) / 2
        segment = segment.translate((mid_x, mid_y, mid_z))
        
        if fin is None:
            fin = segment
        else:
            fin = fin.union(segment)
    
    return fin

# Create all fins
all_fins = None
fin_y_positions = [width / (num_fins + 1) * (i + 1) for i in range(num_fins)]

for y_pos in fin_y_positions:
    fin = create_corrugated_fin(length, fin_height, fin_thickness, amplitude, period)
    fin = fin.translate((0, y_pos, 0))
    
    if all_fins is None:
        all_fins = fin
    else:
        all_fins = all_fins.union(fin)

# Combine base and fins
result = base.union(all_fins)

# Ensure the part is properly formed
result = result.val()

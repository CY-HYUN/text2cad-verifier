import cadquery as cq
import math

# Create the base cubic block with rounded corners
base_size = 60
corner_radius = 15

# Start with a cube
base = cq.Workplane("XY").box(base_size, base_size, base_size)

# Round all edges
base = base.edges().fillet(corner_radius)

# Create the central spherical cavity
sphere_diameter = 40
sphere_radius = sphere_diameter / 2
sphere = cq.Workplane("XY").sphere(sphere_radius)
base = base.cut(sphere)

# Function to create cylindrical pipe with flange
def create_pipe_with_flange(outer_diameter, pipe_length, flange_width, flange_height, is_square=False):
    pipe = cq.Workplane("XY").cylinder(pipe_length, outer_diameter / 2)
    
    if is_square:
        # Square flange for top/bottom
        flange = cq.Workplane("XY").box(flange_width, flange_width, flange_height)
    else:
        # Circular flange for side ports
        flange = cq.Workplane("XY").cylinder(flange_height, flange_width / 2)
    
    # Combine pipe and flange
    assembly = pipe.union(flange.translate((0, 0, pipe_length / 2 + flange_height / 2)))
    return assembly

# Create top inlet pipe (40mm OD, 30mm length, 60x60mm square flange)
top_pipe = create_pipe_with_flange(40, 30, 60, 5, is_square=True)
top_pipe = top_pipe.translate((0, 0, base_size / 2 + 15))

# Create bottom outlet pipe
bottom_pipe = create_pipe_with_flange(40, 30, 60, 5, is_square=True)
bottom_pipe = bottom_pipe.rotate((1, 0, 0), (0, 0, 0), 180)
bottom_pipe = bottom_pipe.translate((0, 0, -base_size / 2 - 15))

# Create front distribution port (30mm OD, 25mm length, 50mm diameter circular flange)
front_pipe = create_pipe_with_flange(30, 25, 50, 5, is_square=False)
front_pipe = front_pipe.rotate((0, 1, 0), (0, 0, 0), 90)
front_pipe = front_pipe.translate((0, base_size / 2 + 12.5, 0))

# Create back distribution port
back_pipe = create_pipe_with_flange(30, 25, 50, 5, is_square=False)
back_pipe = back_pipe.rotate((0, 1, 0), (0, 0, 0), 90)
back_pipe = back_pipe.translate((0, -base_size / 2 - 12.5, 0))

# Create left distribution port
left_pipe = create_pipe_with_flange(30, 25, 50, 5, is_square=False)
left_pipe = left_pipe.rotate((1, 0, 0), (0, 0, 0), 90)
left_pipe = left_pipe.translate((-base_size / 2 - 12.5, 0, 0))

# Create right distribution port
right_pipe = create_pipe_with_flange(30, 25, 50, 5, is_square=False)
right_pipe = right_pipe.rotate((1, 0, 0), (0, 0, 0), 90)
right_pipe = right_pipe.translate((base_size / 2 + 12.5, 0, 0))

# Combine all pipes with base
result = base.union(top_pipe).union(bottom_pipe).union(front_pipe).union(back_pipe).union(left_pipe).union(right_pipe)

# Add triangular reinforcing ribs at corners (simplified as rectangular ribs)
rib_length = 20
rib_width = 8
rib_height = 10

# Create reinforcing ribs at the four top corners
for x_offset in [-base_size/2 + 5, base_size/2 - 5]:
    for y_offset in [-base_size/2 + 5, base_size/2 - 5]:
        rib = cq.Workplane("XY").box(rib_width, rib_width, rib_height)
        rib = rib.translate((x_offset, y_offset, base_size/2 + 2))
        result = result.union(rib)
        
        rib_bottom = cq.Workplane("XY").box(rib_width, rib_width, rib_height)
        rib_bottom = rib_bottom.translate((x_offset, y_offset, -base_size/2 - 2))
        result = result.union(rib_bottom)

# Add bolt holes to flanges (simplified - creating hole patterns)
hole_diameter = 6
hole_positions = [(-15, -15), (-15, 15), (15, -15), (15, 15)]

# Top flange holes
for hx, hy in hole_positions:
    hole = cq.Workplane("XY").cylinder(10, hole_diameter/2)
    hole = hole.translate((hx, hy, base_size/2 + 30 + 5))
    result = result.cut(hole)

# Bottom flange holes
for hx, hy in hole_positions:
    hole = cq.Workplane("XY").cylinder(10, hole_diameter/2)
    hole = hole.translate((hx, hy, -base_size/2 - 30 - 5))
    result = result.cut(hole)

# Side flange holes (circular flanges with 4 holes at 45 degree angles)
for offset_dist in [17.5, -17.5]:
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        hole_x = offset_dist * math.cos(rad)
        hole_y = offset_dist * math.sin(rad)
        
        # Front holes
        hole = cq.Workplane("XY").cylinder(10, hole_diameter/2)
        hole = hole.rotate((1, 0, 0), (0, 0, 0), 90)
        hole = hole.translate((hole_x, base_size/2 + 25 + 5, hole_y))
        result = result.cut(hole)
        
        # Back holes
        hole = cq.Workplane("XY").cylinder(10, hole_diameter/2)
        hole = hole.rotate((1, 0, 0), (0, 0, 0), 90)
        hole = hole.translate((hole_x, -base_size/2 - 25 - 5, hole_y))
        result = result.cut(hole)
        
        # Left holes
        hole = cq.Workplane("XY").cylinder(10, hole_diameter/2)
        hole = hole.rotate((0, 1, 0), (0, 0, 0), 90)
        hole = hole.translate((-base_size/2 - 25 - 5, hole_x, hole_y))
        result = result.cut(hole)
        
        # Right holes
        hole = cq.Workplane("XY").cylinder(10, hole_diameter/2)
        hole = hole.rotate((0, 1, 0), (0, 0, 0), 90)
        hole = hole.translate((base_size/2 + 25 + 5, hole_x, hole_y))
        result = result.cut(hole)

import cadquery as cq
import math

# Create a B-spline curve for the longitudinal spine in the XZ plane
# Start point (0,0,0), end point (110,0,0), with control points at (20,0,35) and (80,0,35)
spine_points = [
    (0, 0, 0),
    (20, 0, 35),
    (80, 0, 35),
    (110, 0, 0)
]

# Create the spine as a spline curve
spine = cq.Workplane("XZ").spline(spine_points)

# Create bottom contour curve in XY plane - asymmetric edge
# This represents the base outline of the mouse
bottom_contour_points = [
    (0, 0, 0),
    (30, 15, 0),
    (70, 20, 0),
    (110, 5, 0),
    (110, -5, 0),
    (70, -20, 0),
    (30, -15, 0),
    (0, 0, 0)
]

# Create the bottom contour as a spline curve
bottom_contour = cq.Workplane("XY").spline(bottom_contour_points)

# Define cross-section profiles at different X positions
# These profiles are arched sections that will be lofted
cross_sections = []

# X-positions for cross-sections
x_positions = [0, 40, 80, 110]

for x_pos in x_positions:
    # Calculate the height from the spine at this X position
    # Using quadratic interpolation for the spine height
    if x_pos <= 55:
        t = x_pos / 55.0
        spine_height = 35 * (2 * t * (1 - t) + t * t)
    else:
        t = (x_pos - 55) / 55.0
        spine_height = 35 * (1 - t) * (1 - t)
    
    # Create an arched profile
    # The profile varies based on position along the length
    width_factor = 0.5 + 0.5 * math.cos(math.pi * x_pos / 110.0)
    
    # Bottom width from contour (approximate asymmetric profile)
    bottom_y_max = 20 * width_factor
    bottom_y_min = -20 * width_factor
    
    # Create profile points: bottom curve to top (spine)
    profile_points = [
        (x_pos, bottom_y_min, 0),
        (x_pos, bottom_y_min * 0.5, spine_height * 0.3),
        (x_pos, 0, spine_height),
        (x_pos, bottom_y_max * 0.5, spine_height * 0.3),
        (x_pos, bottom_y_max, 0)
    ]
    
    # Create wire for this cross-section
    profile_wire = cq.Workplane("YZ").transformed(offset=cq.Vector(x_pos, 0, 0)).spline(
        [(p[1], p[2]) for p in profile_points]
    ).val()
    
    cross_sections.append(profile_wire)

# Create base workplane
result = cq.Workplane("XY")

# Create a lofted surface using the cross-sections
# Start with the first cross-section as a wire
edges = []
for i, x_pos in enumerate(x_positions):
    if x_pos <= 55:
        t = x_pos / 55.0
        spine_height = 35 * (2 * t * (1 - t) + t * t)
    else:
        t = (x_pos - 55) / 55.0
        spine_height = 35 * (1 - t) * (1 - t)
    
    width_factor = 0.5 + 0.5 * math.cos(math.pi * x_pos / 110.0)
    bottom_y_max = 20 * width_factor
    
    profile_points = [
        (x_pos, -20 * width_factor, 0),
        (x_pos, -10 * width_factor, spine_height * 0.3),
        (x_pos, 0, spine_height),
        (x_pos, 10 * width_factor, spine_height * 0.3),
        (x_pos, bottom_y_max, 0)
    ]
    
    edge = cq.Workplane("XYZ").polyline(profile_points).val()
    edges.append(edge)

# Build the lofted solid by creating a shape through lofting
result = cq.Workplane("XY")

# Create profile wires at each X position and loft between them
wires = []
for i, x_pos in enumerate(x_positions):
    if x_pos <= 55:
        t = x_pos / 55.0
        spine_height = 35 * (2 * t * (1 - t) + t * t)
    else:
        t = (x_pos - 55) / 55.0
        spine_height = 35 * (1 - t) * (1 - t)
    
    width_factor = 0.5 + 0.5 * math.cos(math.pi * x_pos / 110.0)
    bottom_y_max = 20 * width_factor
    
    profile_pts = [
        cq.Vector(x_pos, -20 * width_factor, 0),
        cq.Vector(x_pos, -10 * width_factor, spine_height * 0.3),
        cq.Vector(x_pos, 0, spine_height),
        cq.Vector(x_pos, 10 * width_factor, spine_height * 0.3),
        cq.Vector(x_pos, bottom_y_max, 0)
    ]
    
    wire = cq.Workplane("XY").polyline(profile_pts).close().val()
    wires.append(wire)

# Create lofted shell
result = cq.Workplane("XY").loft(wires)

# Thicken the shell inward by 2.0mm to create a solid
result = result.shell(2.0)

# Ensure we have a solid result
if isinstance(result, cq.Workplane):
    result = result.val()

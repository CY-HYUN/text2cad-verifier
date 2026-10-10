import cadquery as cq
import math

def create_spring():
    # Parameters
    num_turns = 5
    radius_bottom = 40.0
    radius_top = 32.5
    height_total = num_turns * 8.0
    rise_per_turn = 8.0
    sine_periods_per_turn = 6
    sine_amplitude = 2.5
    rect_width = 8.0
    rect_thickness = 1.2
    
    # Create the contracting helical path with sinusoidal modulation
    num_points = 500
    points = []
    
    for i in range(num_points):
        t = i / (num_points - 1)  # Parameter from 0 to 1
        
        # Linear radius decrease from bottom to top
        radius = radius_bottom + (radius_top - radius_bottom) * t
        
        # Angular position: 5 full turns over the path
        theta = 2 * math.pi * num_turns * t
        
        # Base axial height: uniform rise
        z_base = height_total * t
        
        # Sinusoidal modulation: 6 periods per turn = 30 periods total
        num_sine_periods = sine_periods_per_turn * num_turns
        sine_phase = 2 * math.pi * num_sine_periods * t
        
        # Decay function: smooth attenuation at start (first quarter) and end (last quarter)
        decay = 1.0
        if t < 0.25:
            # First quarter: decay from 0 to 1
            decay = math.sin(math.pi * t / 0.5) ** 2
        elif t > 0.75:
            # Last quarter: decay from 1 to 0
            decay = math.cos(math.pi * (t - 0.75) / 0.5) ** 2
        
        # Apply sine modulation with decay
        z_sine = sine_amplitude * math.sin(sine_phase) * decay
        
        # Total Z coordinate
        z = z_base + z_sine
        
        # XY coordinates
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        
        points.append(cq.Vector(x, y, z))
    
    # Create path as a BSpline through the points
    path_edge = cq.Edge.makeBSpline(points)
    path_wire = cq.Wire.assembleEdges([path_edge])
    
    # Create the rectangular cross-section
    # Rectangle: width 8.0 mm (horizontal), thickness 1.2 mm (vertical)
    rect_profile = (
        cq.Workplane("XY")
        .rect(rect_width, rect_thickness)
        .wire()
    )
    
    # Use sweep to create the spring solid
    sweep_result = (
        cq.Workplane("XY")
        .sweep(rect_profile, path_wire, normal=cq.Vector(0, 0, 1))
    )
    
    return sweep_result

# Generate the spring
result = create_spring()

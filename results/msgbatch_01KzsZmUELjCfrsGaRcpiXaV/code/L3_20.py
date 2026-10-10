import cadquery as cq
import math

# Create the central hub
hub = cq.Solid.makeCylinder(radius=15, height=20, pnt=cq.Vector(0, 0, 0), dir=cq.Vector(0, 0, 1))

# Create the twisted blade using a lofted surface
# Parameters
blade_length = 60
root_chord = 25
tip_chord = 15
root_angle = 45  # degrees
tip_angle = 15   # degrees
num_sections = 20

# Function to create an airfoil cross-section using cubic Bezier curve
def create_airfoil(chord_length, twist_angle, position_along_blade):
    """Create an airfoil profile as a streamlined shape"""
    # Normalize position from 0 (root) to 1 (tip)
    t = position_along_blade / blade_length
    
    # Taper chord length linearly from root to tip
    current_chord = root_chord - (root_chord - tip_chord) * t
    
    # Interpolate twist angle linearly
    current_angle = root_angle - (root_angle - tip_angle) * t
    
    # Create a streamlined airfoil using a cubic Bezier curve approximation
    # The airfoil is an asymmetric teardrop shape
    # Control points for upper surface
    half_chord = current_chord / 2
    
    # Create points along the airfoil profile (asymmetric teardrop)
    points = []
    for i in range(21):
        s = i / 20.0  # parameter from 0 to 1 along the chord
        
        # Cubic Bezier-like curve for upper surface (thicker leading edge)
        # y = height of airfoil at position s
        if s <= 0.5:
            y_upper = 0.15 * current_chord * (4 * s * (1 - s))
        else:
            y_upper = 0.1 * current_chord * (1 - s) * (1 - s)
        
        # Lower surface (less curved)
        y_lower = -0.08 * current_chord * s * (1 - s)
        
        # Create two sides of the profile
        x = s * current_chord - half_chord
        
        if i <= 10:
            points.append((x, y_upper))
        else:
            points.append((x, y_lower))
    
    # Convert to 3D with twist applied
    points_3d = []
    for x, y in points:
        # Apply twist rotation around the radial axis
        angle_rad = math.radians(current_angle)
        z = position_along_blade
        # Rotate y,z by current angle
        y_rot = y * math.cos(angle_rad) - z * math.sin(angle_rad)
        z_rot = y * math.sin(angle_rad) + z * math.cos(angle_rad)
        points_3d.append(cq.Vector(x, y_rot, z_rot + 10))  # +10 for hub height offset
    
    return points_3d

# Create wire profiles at multiple sections along the blade
wires = []
for i in range(num_sections + 1):
    z_pos = i * blade_length / num_sections
    airfoil_points = create_airfoil(root_chord, root_angle, z_pos)
    
    # Create a wire from the airfoil points
    edge_list = []
    for j in range(len(airfoil_points) - 1):
        edge = cq.Edge.makeLine(airfoil_points[j], airfoil_points[j + 1])
        edge_list.append(edge)
    
    # Close the loop
    edge = cq.Edge.makeLine(airfoil_points[-1], airfoil_points[0])
    edge_list.append(edge)
    
    # Create wire
    wire = cq.Wire.assembleEdges(edge_list)
    wires.append(wire)

# Loft the wires to create the blade surface
blade = cq.Solid.makeLoft(wires)

# Combine hub and blade
result = hub.union(blade)

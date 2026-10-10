import cadquery as cq
import math

# Create a rectangular prism: 80mm long, 50mm wide, 30mm tall
box = cq.Workplane("XY").rect(80.0, 50.0).extrude(30.0)

# The box is centered at origin by default, so we need to shift it to have corners at known positions
# Shift so that one corner is at origin
box = box.translate((40.0, 25.0, 0.0))

# Now the box has corners at:
# Bottom face (Z=0): (0,0,0), (80,0,0), (80,50,0), (0,50,0)
# Top face (Z=30): (0,0,30), (80,0,30), (80,50,30), (0,50,30)

# Upper left front corner is at (0, 0, 30)
# We need to chamfer by cutting a tetrahedron with vertices at:
# (0, 0, 30), (10, 0, 30), (0, 10, 30), (0, 0, 20)

# Create a plane through three points 10mm along each edge from (0, 0, 30)
# Points: (10, 0, 30), (0, 10, 30), (0, 0, 20)
p1_upper = (10.0, 0.0, 30.0)
p2_upper = (0.0, 10.0, 30.0)
p3_upper = (0.0, 0.0, 20.0)

# Create a cutting box for the upper left front corner chamfer
cutting_plane_upper = cq.Workplane("XY").polyline([p1_upper, p2_upper, p3_upper, p1_upper]).close().extrude(-10.0, both=False)

# Lower right rear corner is at (80, 50, 0)
# We need to chamfer by cutting a tetrahedron with vertices at:
# (80, 50, 0), (70, 50, 0), (80, 40, 0), (80, 50, 10)

p1_lower = (70.0, 50.0, 0.0)
p2_lower = (80.0, 40.0, 0.0)
p3_lower = (80.0, 50.0, 10.0)

# Create a cutting box for the lower right rear corner chamfer
cutting_plane_lower = cq.Workplane("XY").polyline([p1_lower, p2_lower, p3_lower, p1_lower]).close().extrude(10.0, both=False)

# More direct approach: use a vertex-based cutting method
# Create the box and chamfer using cut operations with planes

box_shifted = cq.Workplane("XY").rect(80.0, 50.0).extrude(30.0).translate((40.0, 25.0, 0.0))

# For upper left front corner at (0, 0, 30), cut tetrahedron
# Define the plane through (10,0,30), (0,10,30), (0,0,20)
# Normal vector: (1,1,2) normalized or we can use the three points to define a cutting solid

# Create a simple tetrahedral cut using a sketch-based approach
def create_chamfer_solid(p1, p2, p3, p4):
    """Create a solid from 4 points defining a tetrahedron"""
    # We'll use a face and extrude approach
    solid = cq.Workplane("XY").polyline([p1, p2, p3, p1]).close()
    return solid

# Chamfer 1: Upper left front at (0,0,30)
# Cut plane through (10,0,30), (0,10,30), (0,0,20)
box_result = box_shifted.cut(
    cq.Workplane("XY").polyline([(10,0,30), (0,10,30), (0,0,20), (10,0,30)]).close().extrude(10, both=False)
)

# Chamfer 2: Lower right rear at (80,50,0)  
# Cut plane through (70,50,0), (80,40,0), (80,50,10)
result = box_result.cut(
    cq.Workplane("XY").polyline([(70,50,0), (80,40,0), (80,50,10), (70,50,0)]).close().extrude(10, both=False)
)

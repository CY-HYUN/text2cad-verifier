import cadquery as cq
import math

# Create the frustum base
# Bottom square: 80x80 mm, Top square: 50x50 mm, Height: 45 mm
# Center of bottom at origin, Z-axis pointing upward

# Create bottom square (80x80)
bottom_square = cq.Sketch().rect(80, 80)

# Create top square (50x50) at height 45
top_square = cq.Sketch().rect(50, 50)

# Create frustum by lofting between two squares
# First, create a solid by extruding and then lofting
bottom_face = cq.Workplane("XY").workplane(0).rect(80, 80).extrude(0.1)
top_face = cq.Workplane("XY").workplane(45).rect(50, 50).extrude(0.1)

# Better approach: create frustum using two rectangles and loft
part = cq.Workplane("XY").rect(80, 80).workplane(45).rect(50, 50).loft(ruled=True)

# Create the blind cavity (30x30, depth 15mm from top)
# The cavity is at the top surface (z=45) and goes down 15mm
cavity = cq.Workplane("XY").workplane(45).rect(30, 30).pocket(15)

# Apply the cavity to the main part
part = part.cut(cavity)

# Add chamfer to the four top edges of the cavity opening
# The cavity opening is at z=45, and we need to chamfer the top edges
# We need to select the edges that form the top opening of the cavity

# Get edges at the top of the cavity opening and chamfer them
# The cavity opening edges are at z=45, forming a 30x30 square
edges_to_chamfer = part.edges(">Z and <(Z+0.1)").filter(lambda e: abs(e.Center().z - 45) < 1)

# Chamfer with 1mm distance at 45 degrees
result = part.chamfer(1, edges_to_chamfer)


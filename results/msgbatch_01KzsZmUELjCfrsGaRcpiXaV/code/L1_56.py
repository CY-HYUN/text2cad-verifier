import cadquery as cq
import math

# Create the frustum base
# Bottom square: 80x80 mm, Top square: 50x50 mm, Height: 45 mm
# Center of bottom at origin, Z-axis pointing upward

# Create frustum by creating bottom face and lofting to top face
# Start with bottom square (80x80) at z=0
bottom_pts = [
    cq.Vector(-40, -40, 0),
    cq.Vector(40, -40, 0),
    cq.Vector(40, 40, 0),
    cq.Vector(-40, 40, 0)
]

# Top square (50x50) at z=45
top_pts = [
    cq.Vector(-25, -25, 45),
    cq.Vector(25, -25, 45),
    cq.Vector(25, 25, 45),
    cq.Vector(-25, 25, 45)
]

# Create bottom wire
bottom_wire = cq.Wire.makePolygon(bottom_pts)

# Create top wire
top_wire = cq.Wire.makePolygon(top_pts)

# Create frustum by lofting
frustum = cq.Workplane("XY").loft([bottom_wire, top_wire])

# Create blind cavity solid (30x30 square, 15mm deep from z=45 down to z=30)
cavity_solid = (cq.Workplane("XY")
                .workplane(45)
                .rect(30, 30)
                .extrude(-15))

# Cut the cavity from the frustum
part = frustum.cut(cavity_solid)

# Get the top edges of the cavity opening (the edges at z=45 that form the cavity rim)
# These are the edges we need to chamfer
# Filter for edges at the top surface of the cavity
edges_list = part.edges()
cavity_top_edges = edges_list.filter(lambda e: abs(e.Center().z - 45) < 0.5)

# Chamfer the cavity opening edges with 1mm chamfer at 45 degrees
result = part.chamfer(1, cavity_top_edges)

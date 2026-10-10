import cadquery as cq

# Create a wedge-shaped object with a right trapezoidal cross-section
# Base: 80mm (X) x 40mm (Y)
# Height: 30mm at rear (Y=40) and 5mm at front (Y=0)

# Create the wedge by defining a rectangular profile at the front and rear, then lofting
front_profile = cq.Workplane("XZ").rect(80, 5)
rear_profile = cq.Workplane("XZ").transformed(offset=cq.Vector(0, 40, 0)).rect(80, 30)

# Build by creating two rectangular profiles and lofting between them
result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (80, 0), (80, 0), (0, 0)], includeCurrent=False)
    .close()
    .workplane(offset=0)
    .transformed(offset=cq.Vector(0, 0, 0))
)

# Better approach: create solid directly using a box and cut
# Start with a 80x40x30 box, then cut a wedge from the front
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .box(80, 40, 30, centered=False)
)

# Now cut away the excess to create the slope
# Create a cutting tool - a wedge that removes material from Z=5 to Z=30 at the front
cutting_tool = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False)
    .close()
    .extrude(25)
    .translate((0, 0, 5))
)

# We need a different approach - build using vertices and faces
vertices = [
    cq.Vector(0, 0, 0),        # 0: front-left-bottom
    cq.Vector(80, 0, 0),       # 1: front-right-bottom
    cq.Vector(80, 40, 0),      # 2: rear-right-bottom
    cq.Vector(0, 40, 0),       # 3: rear-left-bottom
    cq.Vector(0, 0, 5),        # 4: front-left-top
    cq.Vector(80, 0, 5),       # 5: front-right-top
    cq.Vector(80, 40, 30),     # 6: rear-right-top
    cq.Vector(0, 40, 30),      # 7: rear-left-top
]

# Create faces
bottom = cq.Face.makePolygon([vertices[0], vertices[1], vertices[2], vertices[3]])
front = cq.Face.makePolygon([vertices[0], vertices[1], vertices[5], vertices[4]])
rear = cq.Face.makePolygon([vertices[3], vertices[2], vertices[6], vertices[7]])
left = cq.Face.makePolygon([vertices[0], vertices[3], vertices[7], vertices[4]])
right = cq.Face.makePolygon([vertices[1], vertices[2], vertices[6], vertices[5]])
top = cq.Face.makePolygon([vertices[4], vertices[5], vertices[6], vertices[7]])

# Create shell and make solid
shell = cq.Shell.makeShell([bottom, front, rear, left, right, top])
result = cq.Solid.makeSolid(shell)

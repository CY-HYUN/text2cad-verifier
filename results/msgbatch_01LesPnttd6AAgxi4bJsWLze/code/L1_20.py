import cadquery as cq
import math

# Create a rectangular prism that will be cut diagonally to form the wedge
# Base dimensions: 80mm (X) x 40mm (Y)
# Heights: 30mm at rear (Y=40) and 5mm at front (Y=0)

# Start with a box and then cut it to create the wedge shape
# We'll create a box and use a plane to cut the diagonal

# Create the base box with the maximum height (30mm)
base_box = cq.Workplane("XY").box(80, 40, 30, centered=False)

# Now we need to cut the wedge shape
# The wedge goes from 30mm height at Y=40 to 5mm height at Y=0
# We'll create this by cutting with a plane

# Move box so that its bottom is at Z=0, front is at Y=0, and left side is at X=0
wedge = cq.Workplane("XY").box(80, 40, 30)
# Translate to position: X from 0-80, Y from 0-40, Z from 0-30
wedge = wedge.translate((40, 20, 15))

# Create a cutting plane that removes the excess material
# The plane passes through points creating the slope from 30mm to 5mm
# We need to cut everything above the inclined surface

# The inclined surface goes from (x, 0, 5) to (x, 40, 30) for any x
# This means at Y=0, Z=5 and at Y=40, Z=30
# The slope in Z relative to Y is: (30-5)/(40-0) = 25/40 = 0.625

# Create the wedge by starting with a base and cutting with an inclined plane
wedge_base = cq.Workplane("XY").box(80, 40, 30, centered=False)

# Create a cutting box above the incline to remove excess material
# We'll use a plane cut approach
# The plane equation: Z = 5 + 0.625*Y, or 0.625*Y - Z + 5 = 0

# Instead, let's build it more directly by creating vertices
# Create the wedge shape using vertices
vertices = [
    (0, 0, 0),      # front-left-bottom
    (80, 0, 0),     # front-right-bottom
    (80, 40, 0),    # rear-right-bottom
    (0, 40, 0),     # rear-left-bottom
    (0, 0, 5),      # front-left-top
    (80, 0, 5),     # front-right-top
    (80, 40, 30),   # rear-right-top
    (0, 40, 30),    # rear-left-top
]

# Create faces for the wedge
# Bottom face: vertices 0,1,2,3
# Top inclined face: vertices 4,5,6,7
# Front face: vertices 0,1,5,4
# Rear face: vertices 3,2,6,7
# Left face: vertices 0,3,7,4
# Right face: vertices 1,2,6,5

result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False)
    .close()
    .extrude(5)
    .faces("+Z")
    .workplane()
    .polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False)
    .close()
    .extrude(25)
    .translate((0, 0, -5))
)

# Simpler approach: create using a series of transformations
result = cq.Workplane("XY").box(80, 40, 5)
cutting_wedge = cq.Workplane("XY").box(80, 40, 25, centered=False).translate((0, 0, 5))

# Create the final wedge by combining
result = (
    cq.Workplane("XY")
    .box(80, 40, 30, centered=False)
    .cut(
        cq.Workplane("XY")
        .box(80, 40, 25)
        .translate((0, 20, 17.5))
        .faces(">Y")
        .workplane(offset=-20)
    )
)

# Direct solid creation via vertices
result = cq.Solid.makeSolid(
    cq.Face.makePolygon([
        cq.Vector(0, 0, 0),
        cq.Vector(80, 0, 0),
        cq.Vector(80, 40, 30),
        cq.Vector(0, 40, 30),
    ]).extrude(cq.Vector(0, 0, 5)) if False else
    cq.Workplane("XY")
    .polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False)
    .close()
    .loft([
        cq.Workplane("XY").polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False).close(),
        cq.Workplane("XY").polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False).close().translate((0, 0, 30))
    ], ruled=True)
)

result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False)
    .close()
    .workplane(offset=0)
    .transformed(offset=cq.Vector(0, 0, 25))
    .polyline([(0, 0), (80, 0), (80, 40), (0, 40)], includeCurrent=False)
    .close()
    .loft(ruled=True)
    .translate((0, 0, 5))
)

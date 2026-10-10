import cadquery as cq
import math

# Create the base rectangular prism
base = cq.Workplane("XY").box(80, 50, 30, centered=True)

# The base is centered at origin, so:
# X ranges from -40 to 40
# Y ranges from -25 to 25
# Z ranges from -15 to 15

# Left front upper corner: (-40, -25, 15)
# We need to cut a tetrahedron with edges of 10mm from this corner
# The three edges go along: +X, +Y, -Z directions

# Create a plane at the left front upper corner and define the cutting plane
# The plane passes through three points, each 10mm away from the corner
point1_lfuc = (-40 + 10, -25, 15)  # Along X axis
point2_lfuc = (-40, -25 + 10, 15)  # Along Y axis
point3_lfuc = (-40, -25, 15 - 10)  # Along Z axis

# Right rear lower corner: (40, 25, -15)
# We need to cut a tetrahedron with edges of 10mm from this corner
# The three edges go along: -X, -Y, +Z directions
point1_rruc = (40 - 10, 25, -15)   # Along X axis
point2_rruc = (40, 25 - 10, -15)   # Along Y axis
point3_rruc = (40, 25, -15 + 10)   # Along Z axis

# Cut the left front upper corner
# Create a plane through the three points and cut everything on one side
result = base.cut(
    cq.Workplane("XY")
    .polyline([point1_lfuc, point2_lfuc, point3_lfuc, point1_lfuc])
    .close()
    .extrude(100)  # Extrude far enough to cut through
)

# Cut the right rear lower corner
result = result.cut(
    cq.Workplane("XY")
    .polyline([point1_rruc, point2_rruc, point3_rruc, point1_rruc])
    .close()
    .extrude(100)
)

# Use a more precise approach with cutting planes
base = cq.Workplane("XY").box(80, 50, 30, centered=True)

# Define the cutting plane for left front upper corner using three points
# Create a custom shape by cutting with a plane
def cut_corner_lfuc(shape):
    # Create a box that encompasses the corner to be cut
    # The plane goes through (-30, -15, 5), (-40, -25, 15), (-40, -15, 15)
    cutting_box = (
        cq.Workplane("XY")
        .box(20, 20, 20)
        .translate((-50, -35, 10))
    )
    return shape.cut(cutting_box)

def cut_corner_rruc(shape):
    # Create a box that encompasses the corner to be cut
    cutting_box = (
        cq.Workplane("XY")
        .box(20, 20, 20)
        .translate((50, 35, -20))
    )
    return shape.cut(cutting_box)

# Better approach: use a plane cut
# Left front upper corner at (-40, -25, 15)
plane1_lfuc = cq.Workplane("XY").plane(
    basePnt=(-40 + 10, -25, 15),
    normalVec=(1, 1, -1)
).extrude(50)

result = base
# Cut using a larger solid and plane operations
# Create tetrahedron-like cuts using multiple plane cuts or a polyhedron

# Simpler approach: use faces to define tetrahedra
result = base

# Cut left front upper corner by removing a tetrahedral volume
lfuc_cutter = (
    cq.Workplane("XY")
    .polyline([
        (-40, -25, 15),
        (-30, -25, 15),
        (-40, -15, 15),
        (-40, -25, 5)
    ])
    .close()
    .extrude(10)
)

# Cut right rear lower corner
rruc_cutter = (
    cq.Workplane("XY")
    .polyline([
        (40, 25, -15),
        (30, 25, -15),
        (40, 15, -15),
        (40, 25, -5)
    ])
    .close()
    .extrude(10)
)

result = base.cut(lfuc_cutter).cut(rruc_cutter)

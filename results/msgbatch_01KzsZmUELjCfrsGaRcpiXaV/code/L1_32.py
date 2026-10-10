import cadquery as cq
import math

# Create the base rectangular prism
base = cq.Workplane("XY").box(80, 50, 30, centered=True)

# Left front upper corner: (-40, -25, 15)
# Cut a tetrahedral corner with 10mm edges along X, Y, -Z

# Create a cutting solid for left front upper corner
# Define the tetrahedron by creating a polyline and extruding
lfuc_solid = (
    cq.Workplane("XY")
    .moveTo(-40, -25)
    .polyline([
        (-40, -25),
        (-30, -25),
        (-40, -15),
        (-40, -25)
    ])
    .close()
    .extrude(10, combine=False)
    .val()
)

# Create a cutting plane for the slanted face
# Points: (-30, -25, 15), (-40, -15, 15), (-40, -25, 5)
# Normal vector pointing inward: (1, 1, -1) normalized
lfuc_cutter = (
    cq.Workplane("XY")
    .moveTo(-40, -25)
    .lineTo(-30, -25)
    .lineTo(-40, -15)
    .close()
    .extrude(10)
)

# Right rear lower corner: (40, 25, -15)
# Cut a tetrahedral corner with 10mm edges along -X, -Y, +Z
rruc_cutter = (
    cq.Workplane("XY")
    .moveTo(40, 25)
    .lineTo(30, 25)
    .lineTo(40, 15)
    .close()
    .extrude(10)
    .translate((0, 0, -25))
)

# Apply the cuts
result = base.cut(lfuc_cutter).cut(rruc_cutter)

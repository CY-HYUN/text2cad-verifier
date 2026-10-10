import cadquery as cq
import math

# Create the base three plates oriented along X, Y, Z axes
# Plate dimensions: 50x50x5mm

# Plate 1: XY plane (bottom), centered at origin
plate1 = cq.Workplane("XY").box(50, 50, 5).translate((0, 0, -2.5))

# Plate 2: XZ plane (front), centered at origin
plate2 = cq.Workplane("XZ").box(50, 50, 5).translate((0, -2.5, 0))

# Plate 3: YZ plane (side), centered at origin
plate3 = cq.Workplane("YZ").box(50, 50, 5).translate((-2.5, 0, 0))

# Combine the three plates
result = plate1.union(plate2).union(plate3)

# Cut 15mm diameter holes at the center of each plate
hole_radius = 7.5

# Hole in plate 1 (XY plane)
result = result.faces(">Z").workplane().circle(hole_radius).cutThruAll()

# Hole in plate 2 (XZ plane)
result = result.faces(">Y").workplane().circle(hole_radius).cutThruAll()

# Hole in plate 3 (YZ plane)
result = result.faces(">X").workplane().circle(hole_radius).cutThruAll()

# Create triangular ribs at the three internal corners
# The three corners are where the plates meet at right angles

# Rib 1: At corner where plate1 (XY) and plate2 (XZ) meet (along X axis)
# Triangle in the YZ plane at X=0, with right angle at origin
rib1_points = [(0, 0), (0, 20), (20, 0), (0, 0)]
rib1 = (cq.Workplane("YZ")
        .moveTo(0, 0)
        .polyline(rib1_points)
        .close()
        .extrude(5)
        .translate((0, 0, 0)))

# Rib 2: At corner where plate2 (XZ) and plate3 (YZ) meet (along Z axis)
# Triangle in the XY plane at Z=0, with right angle at origin
rib2_points = [(0, 0), (20, 0), (0, 20), (0, 0)]
rib2 = (cq.Workplane("XY")
        .moveTo(0, 0)
        .polyline(rib2_points)
        .close()
        .extrude(5)
        .translate((0, 0, 0)))

# Rib 3: At corner where plate3 (YZ) and plate1 (XY) meet (along Y axis)
# Triangle in the XZ plane at Y=0, with right angle at origin
rib3_points = [(0, 0), (0, 20), (20, 0), (0, 0)]
rib3 = (cq.Workplane("XZ")
        .moveTo(0, 0)
        .polyline(rib3_points)
        .close()
        .extrude(5)
        .translate((0, 0, 0)))

# Union all ribs with the main structure
result = result.union(rib1).union(rib2).union(rib3)

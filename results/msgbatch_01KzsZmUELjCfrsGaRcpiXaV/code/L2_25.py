import cadquery as cq
import math

# Create the three perpendicular base plates
# Plate 1: XY plane (horizontal at z=0)
plate1 = cq.Workplane("XY").box(50, 50, 5)

# Plate 2: YZ plane (vertical, along Y and Z)
plate2 = cq.Workplane("XY").box(50, 5, 50)

# Plate 3: XZ plane (vertical, along X and Z)
plate3 = cq.Workplane("XY").box(5, 50, 50)

# Combine the three plates at the common vertex
result = plate1.union(plate2).union(plate3)

# Create through-holes at the center of each plate
# Hole through plate1 (XY plane, centered at origin)
hole1 = cq.Workplane("XY").circle(7.5).extrude(100)
result = result.cut(hole1)

# Hole through plate2 (YZ plane, centered at origin)
hole2 = cq.Workplane("YZ").circle(7.5).extrude(100)
result = result.cut(hole2)

# Hole through plate3 (XZ plane, centered at origin)
hole3 = cq.Workplane("XZ").circle(7.5).extrude(100)
result = result.cut(hole3)

# Create triangular reinforcing ribs
# Each rib is a right triangle with legs of 20mm and thickness 5mm

# Rib 1: At the inner corner of XY and YZ planes
# Triangle in the XY plane at the corner, thickness in Z
rib1_points = [(0, 0), (20, 0), (0, 20), (0, 0)]
rib1_profile = cq.Workplane("XY").polyline(rib1_points).close()
rib1 = rib1_profile.extrude(5)
result = result.union(rib1)

# Rib 2: At the inner corner of YZ and XZ planes
# Triangle in the YZ plane at the corner, thickness in X
rib2_points = [(0, 0), (20, 0), (0, 20), (0, 0)]
rib2_profile = cq.Workplane("YZ").polyline(rib2_points).close()
rib2 = rib2_profile.extrude(5)
result = result.union(rib2)

# Rib 3: At the inner corner of XZ and XY planes
# Triangle in the XZ plane at the corner, thickness in Y
rib3_points = [(0, 0), (20, 0), (0, 20), (0, 0)]
rib3_profile = cq.Workplane("XZ").polyline(rib3_points).close()
rib3 = rib3_profile.extrude(5)
result = result.union(rib3)

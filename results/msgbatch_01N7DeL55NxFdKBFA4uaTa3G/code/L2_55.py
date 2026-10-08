import cadquery as cq
import math

R = 50.0          # path arc radius
d_start = 30.0    # start circle diameter
d_end = 15.0      # end circle diameter

# Path: 90-degree arc in the front (XZ) plane
# Center at (R, 0, 0); starts at origin heading +Z, ends at (R, 0, R) heading +X
mid = (R - R * math.cos(math.radians(45)), R * math.sin(math.radians(45)))
path = cq.Workplane("XZ").moveTo(0, 0).threePointArc(mid, (R, R))
path_wire = path.val() if isinstance(path.val(), cq.Wire) else cq.Wire.assembleEdges(path.vals())

# Reference planes at start and end of path, with circle profiles
w_start = cq.Wire.makeCircle(d_start / 2.0, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
w_end = cq.Wire.makeCircle(d_end / 2.0, cq.Vector(R, 0, R), cq.Vector(1, 0, 0))

try:
    # Loft with centerline (multi-section sweep along the arc)
    solid = cq.Solid.sweep_multi([w_start, w_end], path_wire, True, False)
    if not solid.isValid():
        raise ValueError
    result = cq.Workplane("XY").add(solid)
except Exception:
    # Fallback: loft through intermediate sections placed along the arc centerline
    n = 12
    wires = []
    for i in range(n + 1):
        t = i / n
        a = math.radians(90.0 * t)
        # point on arc (center at (R,0,0))
        p = cq.Vector(R - R * math.cos(a), 0, R * math.sin(a))
        # tangent direction
        tan = cq.Vector(math.sin(a), 0, math.cos(a))
        r = (d_start + (d_end - d_start) * t) / 2.0
        wires.append(cq.Wire.makeCircle(r, p, tan))
    solid = cq.Solid.makeLoft(wires, False)
    result = cq.Workplane("XY").add(solid)

import cadquery as cq
import math

outer = cq.Workplane("XY").box(60, 60, 60)
cavity = cq.Workplane("XY").box(52, 52, 52)
shell = outer.cut(cavity)
core = cq.Workplane("XY").box(20, 20, 20)

result = shell.union(core)

# rods: from x=9 to x=27 (overlapping into core and wall)
length = 18
center = 18
for axis in ("X", "Y", "Z"):
    for s in (1, -1):
        if axis == "X":
            wp = cq.Workplane("YZ")
            pos = cq.Vector(s * center, 0, 0)
            rod = cq.Workplane("YZ").workplane(offset=0).center(0, 0).circle(1).extrude(length / 2, both=True)
            rod = rod.translate(pos)
        elif axis == "Y":
            rod = cq.Workplane("XZ").circle(1).extrude(length / 2, both=True)
            rod = rod.translate(cq.Vector(0, s * center, 0))
        else:
            rod = cq.Workplane("XY").circle(1).extrude(length / 2, both=True)
            rod = rod.translate(cq.Vector(0, 0, s * center))
        result = result.union(rod)

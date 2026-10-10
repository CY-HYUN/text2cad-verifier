import cadquery as cq
import math

a = 50.0
cube = cq.Workplane("XY").box(a, a, a, centered=False)

# body diagonal from (0,0,0) to (a,a,a)
start = cq.Vector(0, 0, 0)
end = cq.Vector(a, a, a)
d = end - start
length = d.Length
direction = d.normalized()

# cylinder longer than the diagonal, centered on the diagonal
cyl_len = length + 20
base = start - direction * 10
cyl = cq.Solid.makeCylinder(5.0, cyl_len, base, direction)

result = cube.cut(cq.Workplane("XY").add(cyl))

import cadquery as cq

# Outer cube 60mm, shelled inward 5mm with no faces removed (closed hollow box)
outer = cq.Workplane("XY").box(60, 60, 60)
cavity = cq.Workplane("XY").box(50, 50, 50)
shell = outer.cut(cavity)

# Inner small cube 20mm at center
inner = cq.Workplane("XY").box(20, 20, 20)

# Rods: 2mm diameter from each face center of the small cube to the inner shell wall
r = 1.0
start = 9.0   # slightly inside small cube for robust union
end = 26.0    # slightly into the wall (inner wall at 25)
length = end - start

rods = None
dirs = [
    ((1, 0, 0)), ((-1, 0, 0)),
    ((0, 1, 0)), ((0, -1, 0)),
    ((0, 0, 1)), ((0, 0, -1)),
]
for d in dirs:
    base = cq.Vector(d[0] * start, d[1] * start, d[2] * start)
    cyl = cq.Solid.makeCylinder(r, length, base, cq.Vector(*d))
    rods = cyl if rods is None else rods.fuse(cyl)

result = shell.union(inner).union(cq.Workplane("XY").add(rods))
result = result.clean()

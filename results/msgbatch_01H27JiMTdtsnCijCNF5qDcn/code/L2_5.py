import cadquery as cq
import math

R_out = 10.0      # 20 mm diameter
wall = 2.0
R_in = R_out - wall
L_main = 100.0
L_branch = 100.0
half_angle = 30.0  # each branch 30° from vertical -> 60° between branches

a = math.radians(half_angle)
junction = cq.Vector(0, 0, L_main)
dirs = [cq.Vector(math.sin(a), 0, math.cos(a)),
        cq.Vector(-math.sin(a), 0, math.cos(a))]


def sweep_seg(radius, start, direction, length):
    end = start + direction * length
    edge = cq.Edge.makeLine(start, end)
    wire = cq.Wire.assembleEdges([edge])
    path = cq.Workplane("XY").newObject([wire])
    plane = cq.Plane(origin=(start.x, start.y, start.z),
                     xDir=(0, 1, 0),
                     normal=(direction.x, direction.y, direction.z))
    return cq.Workplane(plane).circle(radius).sweep(path)


def build(radius, ext):
    # main path (vertical)
    body = sweep_seg(radius, cq.Vector(0, 0, -ext), cq.Vector(0, 0, 1), L_main + ext)
    # smooth blending at the branching point
    body = body.union(cq.Workplane("XY").sphere(radius).translate((0, 0, L_main)))
    # two branches
    for d in dirs:
        body = body.union(sweep_seg(radius, junction, d, L_branch + ext))
    return body


outer = build(R_out, 0.0)
inner = build(R_in, 1.0)   # extended so the three end faces are opened

result = outer.cut(inner)

import cadquery as cq
import math

R_out = 10.0      # 20 mm diameter profile
wall = 2.0        # uniform wall thickness
R_in = R_out - wall
L_main = 60.0
L_branch = 50.0
half = math.radians(30)  # branches 60 deg apart -> +/-30 deg from vertical

J = cq.Vector(0, 0, L_main)
dirs = [cq.Vector(math.sin(half), 0, math.cos(half)),
        cq.Vector(-math.sin(half), 0, math.cos(half))]


def sweep_segment(p0, p1, r):
    d = (p1 - p0).normalized()
    # pick an xDir perpendicular to d
    ref = cq.Vector(0, 1, 0) if abs(d.y) < 0.9 else cq.Vector(1, 0, 0)
    xd = ref.cross(d).normalized()
    plane = cq.Plane(origin=p0, xDir=xd, normal=d)
    path = cq.Wire.makePolygon([p0, p1])
    return cq.Workplane(plane).circle(r).sweep(path)


def y_body(r, ext):
    # main path: vertical from origin to junction
    body = sweep_segment(cq.Vector(0, 0, -ext), J, r)
    # two branches
    for d in dirs:
        body = body.union(sweep_segment(J, J + d * (L_branch + ext), r))
    # smooth merge at the branching point
    body = body.union(cq.Workplane("XY").sphere(r).translate(J.toTuple()))
    return body


outer = y_body(R_out, 0.0)
# inner void extends past the three end faces so they are removed (open ends)
inner = y_body(R_in, 1.0)

result = outer.cut(inner)

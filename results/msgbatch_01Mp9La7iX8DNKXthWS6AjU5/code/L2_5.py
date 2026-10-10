import cadquery as cq
import math

R_out = 10.0       # 20 mm diameter
wall = 2.0
R_in = R_out - wall
H = 100.0          # main trunk length
L = 80.0           # branch length
half = math.radians(30.0)   # each branch 30 deg from vertical -> 60 deg between branches


def y_pipe(r, ext=0.0):
    # main trunk (swept along vertical path)
    main_path = cq.Workplane("XZ").moveTo(0, -ext).lineTo(0, H)
    main = (cq.Workplane("XY").workplane(offset=-ext)
            .circle(r).sweep(main_path))
    body = main
    # smooth blend at the junction
    body = body.union(cq.Workplane("XY").sphere(r).translate((0, 0, H)))
    for s in (1, -1):
        d = cq.Vector(s * math.sin(half), 0, math.cos(half))
        l = L + ext
        end = (s * l * math.sin(half), H + l * math.cos(half))
        path = cq.Workplane("XZ").moveTo(0, H).lineTo(*end)
        pl = cq.Plane(origin=(0, 0, H), xDir=(0, 1, 0), normal=d.toTuple())
        br = cq.Workplane(pl).circle(r).sweep(path)
        body = body.union(br)
    return body


outer = y_pipe(R_out)
inner = y_pipe(R_in, ext=2.0)
# hollow with uniform wall, all three end faces open
result = outer.cut(inner)

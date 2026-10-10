import cadquery as cq
import math

def bez(t):
    x = 3*(1-t)*t**2*60 + t**3*60
    z = 3*(1-t)**2*t*60 + 3*(1-t)*t**2*60 + t**3*120
    return x, z

def make_loft(off):
    wires = []
    n = 10
    for i in range(n + 1):
        t = i / n
        x, z = bez(t)
        a = 60 + (30 - 60) * t - off
        b = 40 + (30 - 40) * t - off
        wp = cq.Workplane("XY").workplane(offset=z).center(x, 0)
        if abs(a - b) < 1e-9:
            w = wp.circle(a).val()
        else:
            w = wp.ellipse(a, b).val()
        wires.append(w)
    return cq.Workplane("XY").add(cq.Solid.makeLoft(wires, False))

outer = make_loft(0)
inner = make_loft(3)
shell = outer.cut(inner)

flange = (cq.Workplane("XY").workplane(offset=120).center(60, 0)
          .circle(35).circle(27).extrude(2))

result = shell.union(flange)

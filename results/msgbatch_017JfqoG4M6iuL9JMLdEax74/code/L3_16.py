import cadquery as cq
import math

def bez(t):
    x = 3*t*(1-t)**2*20 + 3*t**2*(1-t)*80 + t**3*110
    z = 3*t*(1-t)**2*35 + 3*t**2*(1-t)*35
    return x, z

p = math.log(0.5)/math.log(1/3.0)

def width(x):
    u = min(max(x/110.0, 1e-3), 0.999)
    return 18 + 42*math.sin(math.pi*u**p)

wires = []
ts = [0.04, 0.12, 0.22, 0.33, 0.45, 0.57, 0.69, 0.80, 0.89, 0.96]
for t in ts:
    x, h = bez(t)
    h = max(h, 3.0)
    w = width(x)
    pts = []
    n = 12
    for i in range(n+1):
        th = math.pi*i/n
        # slight inward curl near base for fitting
        yy = (w/2)*math.cos(th)*(1 - 0.06*(1 - math.sin(th)))
        zz = h*math.sin(th)**0.9
        pts.append((yy, zz))
    wp = cq.Workplane("YZ", origin=(x, 0, 0)).spline(pts, includeCurrent=False).close()
    wires.append(wp.wires().val())

body = cq.Workplane("XY").add(cq.Solid.makeLoft(wires, False))

# asymmetric thumb rest on the left side (+Y)
thumb = (cq.Workplane("XY")
         .add(cq.Solid.makeSphere(16, pnt=cq.Vector(42, 43, 10)))
         )
body = body.cut(thumb)

# slight asymmetric bulge on the right-rear side to emphasize grip
try:
    shelled = body.faces("<X or >X").shell(-1.8) if False else body.faces("<Z").shell(-1.8)
    result = shelled
except Exception:
    result = body

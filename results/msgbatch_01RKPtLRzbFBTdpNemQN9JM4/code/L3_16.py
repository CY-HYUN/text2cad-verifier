import cadquery as cq
import math

# Longitudinal spine: cubic Bezier in the XZ plane
P = [(0, 0), (20, 35), (80, 35), (110, 0)]

def bez(t):
    mt = 1 - t
    x = mt**3*P[0][0] + 3*mt*mt*t*P[1][0] + 3*mt*t*t*P[2][0] + t**3*P[3][0]
    z = mt**3*P[0][1] + 3*mt*mt*t*P[1][1] + 3*mt*t*t*P[2][1] + t**3*P[3][1]
    return x, z

samples = [bez(i/400.0) for i in range(401)]

def height(x):
    for i in range(len(samples)-1):
        x0, z0 = samples[i]
        x1, z1 = samples[i+1]
        if x0 <= x <= x1:
            f = 0 if x1 == x0 else (x-x0)/(x1-x0)
            return z0 + f*(z1-z0)
    return 0.0

def half_width(x):
    u = min(max(x/110.0, 0.0), 1.0)
    w = 4 + 56*math.sin(math.pi*u**1.71)   # widest near the rear third (~x=73)
    return w/2.0

def yshift(x):
    u = min(max(x/110.0, 0.0), 1.0)
    return 1.5*math.sin(math.pi*u)  # slight asymmetry

def build(xs, da, db, amin, bmin):
    wp = None
    for x in xs:
        a = max(half_width(x)-da, amin)
        b = max(height(x)*1.0-db, bmin)
        if wp is None:
            wp = cq.Workplane("YZ").workplane(offset=x).center(yshift(x), 0).ellipse(a, b)
        else:
            wp = wp.workplane(offset=x-prev).center(yshift(x)-yprev, 0).ellipse(a, b)
        globals()['prev'] = x
        globals()['yprev'] = yshift(x)
    return wp.loft(ruled=False, combine=True)

xs_out = [0.5, 10, 22, 35, 48, 60, 73, 85, 97, 109.5]
outer = build(xs_out, 0, 0, 4, 3)

# keep only the upper half (base plane at z=0)
box = cq.Workplane("XY").box(120, 80, 40, centered=(False, True, False)).translate((-5, 0, 0))
outer = outer.intersect(box)

# concave thumb rest on the left side (-Y)
thumb = cq.Workplane("XY").sphere(8).translate((35, -19, 12))
outer = outer.cut(thumb)

# hollow underside
xs_in = [3, 12, 22, 35, 48, 60, 73, 85, 97, 107]
inner = build(xs_in, 2, 2, 2, 1)

result = outer.cut(inner)

import cadquery as cq
import math

a = 3.0          # base circle radius
t = 4.0          # wall thickness
h = 25.0         # wall height
plate_d = 80.0
plate_t = 5.0
half = t / 2.0

phi0 = 1.0               # start where curvature radius > half thickness (smooth offset)
phi1 = 6 * math.pi       # 1080 deg
N = 600

def P(phi):
    return (a * (math.cos(phi) + phi * math.sin(phi)),
            a * (math.sin(phi) - phi * math.cos(phi)))

def nrm(phi):
    return (-math.sin(phi), math.cos(phi))

def tan(phi):
    return (math.cos(phi), math.sin(phi))

phis = [phi0 + (phi1 - phi0) * i / N for i in range(N + 1)]
outer = []
inner = []
for p in phis:
    x, y = P(p)
    nx, ny = nrm(p)
    outer.append((x + half * nx, y + half * ny))
    inner.append((x - half * nx, y - half * ny))

# start cap semicircle (radius 2) tangent to both wall sides
cx, cy = P(phi0)
tx, ty = tan(phi0)
cap_mid = (cx - half * tx, cy - half * ty)

wp = cq.Workplane("XY").workplane(offset=plate_t).moveTo(*outer[0])
wp = wp.spline(outer[1:], includeCurrent=True)
wp = wp.lineTo(*inner[-1])
wp = wp.spline(list(reversed(inner))[1:], includeCurrent=True)
wp = wp.threePointArc(cap_mid, outer[0])
wall = wp.close().extrude(h)

# keep the wall on the plate footprint
clip = cq.Workplane("XY").circle(plate_d / 2.0).extrude(plate_t + h + 1)
wall = wall.intersect(clip)

plate = cq.Workplane("XY").circle(plate_d / 2.0).extrude(plate_t)

result = plate.union(wall)

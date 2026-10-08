import cadquery as cq
import math

# Cylinder parameters
D = 30.0
R = D / 2.0
L = 60.0

# Knurl parameters
helix_angle = 30.0                     # degrees from the cylinder axis
pitch = math.pi * D / math.tan(math.radians(helix_angle))
n_grooves = 18                         # grooves per direction
depth = 0.8                            # V-groove depth
half_w = 0.8                           # half width of the V at the surface
ext = 5.0                              # extend the path past both ends
z0 = -ext
h = L + 2 * ext

# Base cylinder
cyl = cq.Workplane("XY").circle(R).extrude(L)


def groove(lefthand):
    helix = cq.Wire.makeHelix(pitch, h, R, center=cq.Vector(0, 0, z0),
                              lefthand=lefthand)
    # V profile in a plane normal to the axis at the helix start point (R,0,z0)
    pts = [
        (R + 1.0, -half_w - 1.0 * half_w / depth),
        (R + 1.0, half_w + 1.0 * half_w / depth),
        (R - depth, 0.0),
    ]
    prof = cq.Workplane("XY", origin=(0, 0, z0)).polyline(pts).close()
    return prof.sweep(cq.Workplane(obj=helix), isFrenet=True).val()


tools = []
for lh in (False, True):
    g = groove(lh)
    for i in range(n_grooves):
        tools.append(g.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1),
                              i * 360.0 / n_grooves))

result = cyl.cut(cq.Workplane(obj=cq.Compound.makeCompound(tools)))

import cadquery as cq

L = 100
R = 20
t = 2

def cross(r, length):
    a = cq.Workplane("YZ").circle(r).extrude(length / 2, both=True)  # along X
    b = cq.Workplane("XZ").circle(r).extrude(length / 2, both=True)  # along Y
    return a.union(b)

outer = cross(R, L)
inner = cross(R - t, L + 2)
result = outer.cut(inner)

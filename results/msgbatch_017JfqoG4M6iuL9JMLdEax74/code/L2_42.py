import cadquery as cq

T = 10.0
L = 100.0
W = 60.0
leg = 50.0
hole_d = 20.0

# Horizontal plate (XY), vertical plate (YZ)
horiz = cq.Workplane("XY").box(L, W, T, centered=False)
vert = cq.Workplane("XY").box(T, W, L, centered=False)

# Triangular gusset in XZ plane, centered in Y
gusset = (
    cq.Workplane("XZ", origin=(0, W / 2 + T / 2, 0))
    .polyline([(T, T), (T + leg, T), (T, T + leg)])
    .close()
    .extrude(T)
)

body = horiz.union(vert).union(gusset)

# Through holes at plate centers
hole_h = (
    cq.Workplane("XY")
    .center(L / 2, W / 2)
    .circle(hole_d / 2)
    .extrude(T * 3)
    .translate((0, 0, -T))
)
hole_v = (
    cq.Workplane("YZ")
    .center(W / 2, L / 2)
    .circle(hole_d / 2)
    .extrude(T * 3)
    .translate((-T, 0, 0))
)

result = body.cut(hole_h).cut(hole_v)

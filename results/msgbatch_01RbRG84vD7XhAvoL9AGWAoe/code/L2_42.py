import cadquery as cq

L = 100.0   # plate length (X)
W = 60.0    # plate width
T = 10.0    # plate thickness
leg = 50.0  # gusset leg length
gt = 10.0   # gusset thickness
hole_d = 20.0

# Horizontal plate: X [-50,50], Y [0,60], Z [0,10]
horiz = cq.Workplane("XY").box(L, W, T, centered=(True, False, False))

# Vertical plate: X [-50,50], Y [0,10], Z [0,60]
vert = cq.Workplane("XY").box(L, T, W, centered=(True, False, False))

body = horiz.union(vert)

# Triangular gusset in the inner corner, centered in X
gusset = (
    cq.Workplane("YZ")
    .polyline([(T, T), (T + leg, T), (T, T + leg)])
    .close()
    .extrude(gt / 2.0, both=True)
)
body = body.union(gusset)

# Through-hole in horizontal plate (vertical axis) at plate center
h_hole = (
    cq.Workplane("XY")
    .center(0, W / 2.0)
    .circle(hole_d / 2.0)
    .extrude(W + 10)
    .translate((0, 0, -5))
)

# Through-hole in vertical plate (axis along Y) at plate center
v_hole = (
    cq.Workplane("XZ")
    .center(0, W / 2.0)
    .circle(hole_d / 2.0)
    .extrude(-(W + 10))
    .translate((0, -5, 0))
)

result = body.cut(h_hole).cut(v_hole)

import cadquery as cq

L = 100.0   # plate length
T = 10.0    # plate thickness
W = 60.0    # extrusion width (Y)
RIB_LEG = 50.0
RIB_T = 10.0
HOLE_D = 20.0

# L-shaped body: horizontal plate (along X) + vertical plate (along Z)
horiz = cq.Workplane("XY").box(L, W, T, centered=False)
vert = cq.Workplane("XY").box(T, W, L, centered=False)
body = horiz.union(vert)

# Rib: right triangle in XZ plane at the mid-plane (y = W/2), connecting inner walls
rib_pts = [(T, T), (T + RIB_LEG, T), (T, T + RIB_LEG)]
rib = (
    cq.Workplane("XZ", origin=(0, W / 2 + RIB_T / 2, 0))
    .polyline(rib_pts).close()
    .extrude(RIB_T)  # XZ normal is -Y, so this spans y = W/2 - RIB_T/2 .. W/2 + RIB_T/2
)
body = body.union(rib)

# Hole through horizontal plate (center of plate)
h_hole = (
    cq.Workplane("XY")
    .center(L / 2, W / 2)
    .circle(HOLE_D / 2)
    .extrude(L + 10)
    .translate((0, 0, -5))
)
# Hole through vertical plate (center of plate)
v_hole = (
    cq.Workplane("YZ")
    .center(W / 2, L / 2)
    .circle(HOLE_D / 2)
    .extrude(L + 10)
    .translate((-5, 0, 0))
)

result = body.cut(h_hole).cut(v_hole)

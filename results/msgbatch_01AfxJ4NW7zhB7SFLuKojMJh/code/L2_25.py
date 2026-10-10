import cadquery as cq

t = 5.0
L = 50.0

# Three plates sharing the corner at the origin
p_xy = cq.Workplane("XY").box(L, L, t, centered=False)
p_yz = cq.Workplane("XY").box(t, L, L, centered=False)
p_xz = cq.Workplane("XY").box(L, t, L, centered=False)
body = p_xy.union(p_yz).union(p_xz)

# Triangular ribs (legs 20 mm, thickness 5 mm) at each inner edge
pts = [(5, 5), (25, 5), (5, 25)]
rib_x = cq.Workplane("YZ").workplane(offset=5).polyline(pts).close().extrude(5)
rib_y = cq.Workplane("XZ").workplane(offset=-10).polyline(pts).close().extrude(5)
rib_z = cq.Workplane("XY").workplane(offset=5).polyline(pts).close().extrude(5)
body = body.union(rib_x).union(rib_y).union(rib_z)

# 15 mm through-holes at the centre of each plate
r = 7.5
h_xy = cq.Workplane("XY").workplane(offset=-1).center(25, 25).circle(r).extrude(t + 2)
h_yz = cq.Workplane("YZ").workplane(offset=-1).center(25, 25).circle(r).extrude(t + 2)
h_xz = cq.Workplane("XZ").workplane(offset=-(t + 1)).center(25, 25).circle(r).extrude(t + 2)
body = body.cut(h_xy).cut(h_yz).cut(h_xz)

result = body

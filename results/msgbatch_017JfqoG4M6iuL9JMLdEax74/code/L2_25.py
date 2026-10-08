import cadquery as cq

L = 50.0   # plate size
T = 5.0    # plate thickness
D = 15.0   # hole diameter
R = 20.0   # rib leg length
RT = 5.0   # rib thickness

# Three mutually perpendicular plates sharing the origin vertex
p_xy = cq.Workplane("XY").box(L, L, T, centered=False)
p_yz = cq.Workplane("XY").box(T, L, L, centered=False)
p_xz = cq.Workplane("XY").box(L, T, L, centered=False)

body = p_xy.union(p_yz).union(p_xz)

# Center through-holes
h_xy = cq.Workplane("XY").center(L / 2, L / 2).circle(D / 2).extrude(T)
h_yz = cq.Workplane("YZ").center(L / 2, L / 2).circle(D / 2).extrude(T)
h_xz = (cq.Workplane("XZ", origin=(0, T, 0))
        .center(L / 2, L / 2).circle(D / 2).extrude(T))
body = body.cut(h_xy).cut(h_yz).cut(h_xz)

tri = [(T, T), (T + R, T), (T, T + R)]

# Rib along X edge (between XY and XZ plates), at far end
rib_x = (cq.Workplane("YZ", origin=(L - RT, 0, 0))
         .polyline(tri).close().extrude(RT))
# Rib along Y edge (between XY and YZ plates), at far end
rib_y = (cq.Workplane("XZ", origin=(0, L, 0))
         .polyline(tri).close().extrude(RT))
# Rib along Z edge (between YZ and XZ plates), at far end
rib_z = (cq.Workplane("XY", origin=(0, 0, L - RT))
         .polyline(tri).close().extrude(RT))

result = body.union(rib_x).union(rib_y).union(rib_z)

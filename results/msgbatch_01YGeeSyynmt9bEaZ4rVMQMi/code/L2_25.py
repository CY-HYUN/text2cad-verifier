import cadquery as cq

L = 50.0   # plate size
T = 5.0    # plate thickness
D = 15.0   # hole diameter
R = 20.0   # rib leg length
RT = 5.0   # rib thickness

# Plates
p_xy = cq.Workplane("XY").box(L, L, T, centered=False)  # floor (z 0..5)
p_xz = cq.Workplane("XY").box(L, T, L, centered=False)  # wall, y 0..5
p_yz = cq.Workplane("XY").box(T, L, L, centered=False)  # wall, x 0..5

# Holes at the centre of each plate
h_xy = cq.Workplane("XY").center(L / 2, L / 2).circle(D / 2).extrude(T)
h_xz = (cq.Workplane("XZ").center(L / 2, L / 2).circle(D / 2)
        .extrude(-T))
h_yz = cq.Workplane("YZ").center(L / 2, L / 2).circle(D / 2).extrude(T)

body = p_xy.union(p_xz).union(p_yz).cut(h_xy).cut(h_xz).cut(h_yz)

c = L / 2 - RT / 2  # rib start so it is centred on the plate

# Rib along X edge (between XY and XZ plates), triangle in YZ plane
rib_x = (cq.Workplane("YZ", origin=(c, 0, 0))
         .polyline([(T, T), (T + R, T), (T, T + R)]).close()
         .extrude(RT))

# Rib along Y edge (between XY and YZ plates), triangle in XZ plane
rib_y = (cq.Workplane("XZ", origin=(0, c + RT, 0))
         .polyline([(T, T), (T + R, T), (T, T + R)]).close()
         .extrude(RT))

# Rib along Z edge (between XZ and YZ plates), triangle in XY plane
rib_z = (cq.Workplane("XY", origin=(0, 0, c))
         .polyline([(T, T), (T + R, T), (T, T + R)]).close()
         .extrude(RT))

result = body.union(rib_x).union(rib_y).union(rib_z)

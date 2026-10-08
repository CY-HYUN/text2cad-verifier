import cadquery as cq

L = 50.0
T = 5.0
HOLE_D = 15.0
RIB = 20.0
RIB_T = 5.0
mid = L / 2.0

# Three plates forming an internal corner
plate_xy = cq.Workplane("XY").box(L, L, T, centered=False)                  # z in [0,5]
plate_xz = cq.Workplane("XY").box(L, T, L, centered=False)                  # y in [0,5]
plate_yz = cq.Workplane("XY").box(T, L, L, centered=False)                  # x in [0,5]

body = plate_xy.union(plate_xz).union(plate_yz)

# Rib along X edge (between XY and XZ plates), triangle in YZ plane
rib_x = (cq.Workplane("YZ").workplane(offset=mid - RIB_T / 2)
         .polyline([(T, T), (T + RIB, T), (T, T + RIB)]).close()
         .extrude(RIB_T))

# Rib along Y edge (between XY and YZ plates), triangle in XZ plane (normal -Y)
rib_y = (cq.Workplane("XZ").workplane(offset=-(mid + RIB_T / 2))
         .polyline([(T, T), (T + RIB, T), (T, T + RIB)]).close()
         .extrude(RIB_T))

# Rib along Z edge (between XZ and YZ plates), triangle in XY plane
rib_z = (cq.Workplane("XY").workplane(offset=mid - RIB_T / 2)
         .polyline([(T, T), (T + RIB, T), (T, T + RIB)]).close()
         .extrude(RIB_T))

body = body.union(rib_x).union(rib_y).union(rib_z)

# Central holes in each plate
r = HOLE_D / 2.0
h_xy = cq.Solid.makeCylinder(r, T + 2, cq.Vector(mid, mid, -1), cq.Vector(0, 0, 1))
h_xz = cq.Solid.makeCylinder(r, T + 2, cq.Vector(mid, -1, mid), cq.Vector(0, 1, 0))
h_yz = cq.Solid.makeCylinder(r, T + 2, cq.Vector(-1, mid, mid), cq.Vector(1, 0, 0))

result = body.cut(cq.Workplane().add(h_xy)).cut(cq.Workplane().add(h_xz)).cut(cq.Workplane().add(h_yz))

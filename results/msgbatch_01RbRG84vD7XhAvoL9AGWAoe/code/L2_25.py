import cadquery as cq

L = 50.0
T = 5.0
HOLE_D = 15.0
RIB = 20.0
RIB_T = 5.0
RIB_POS = 40.0  # rib placed near outer end of each edge, clear of the holes

# Three perpendicular plates sharing a common vertex at origin
plate_xy = cq.Workplane("XY").box(L, L, T, centered=False)
plate_yz = cq.Workplane("XY").box(T, L, L, centered=False)
plate_xz = cq.Workplane("XY").box(L, T, L, centered=False)

body = plate_xy.union(plate_yz).union(plate_xz)

# Center through-holes in each plate
hole_z = cq.Workplane("XY").center(L / 2, L / 2).circle(HOLE_D / 2).extrude(T * 3).translate((0, 0, -T))
hole_x = cq.Workplane("YZ").center(L / 2, L / 2).circle(HOLE_D / 2).extrude(T * 3).translate((-T, 0, 0))
hole_y = cq.Workplane("XZ").center(L / 2, L / 2).circle(HOLE_D / 2).extrude(-T * 3).translate((0, -T, 0))
body = body.cut(hole_z).cut(hole_x).cut(hole_y)

# Triangular ribs at each inner right angle
tri = [(T, T), (T + RIB, T), (T, T + RIB)]

# Rib between XY and XZ plates (edge along X)
rib_x = cq.Workplane("YZ", origin=(RIB_POS, 0, 0)).polyline(tri).close().extrude(RIB_T)
# Rib between XY and YZ plates (edge along Y); XZ normal is -Y
rib_y = cq.Workplane("XZ", origin=(0, RIB_POS + RIB_T, 0)).polyline(tri).close().extrude(RIB_T)
# Rib between YZ and XZ plates (edge along Z)
rib_z = cq.Workplane("XY", origin=(0, 0, RIB_POS)).polyline(tri).close().extrude(RIB_T)

result = body.union(rib_x).union(rib_y).union(rib_z)

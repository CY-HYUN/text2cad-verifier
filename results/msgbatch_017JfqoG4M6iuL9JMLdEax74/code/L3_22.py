import cadquery as cq
import math

# ---------------- parameters ----------------
R_bot_out, R_bot_in, t_bot = 30.0, 25.0, 4.0
R_top, t_top = 20.0, 4.0
H = 40.0
r_strut = 2.0
n_strut = 8
z_mid = H / 2.0

# ---------------- bottom mounting ring ----------------
bottom = (cq.Workplane("XY").circle(R_bot_out).circle(R_bot_in).extrude(t_bot))

# four lugs with M4 holes
lug_r = 34.0
for i in range(4):
    a = math.radians(45 + 90 * i)
    cx, cy = lug_r * math.cos(a), lug_r * math.sin(a)
    lug = (cq.Workplane("XY")
           .center(cx, cy).circle(5.5).extrude(t_bot))
    neck = (cq.Workplane("XY")
            .transformed(rotate=(0, 0, 45 + 90 * i))
            .center(30.0, 0).rect(9.0, 11.0).extrude(t_bot))
    bottom = bottom.union(lug).union(neck)
for i in range(4):
    a = math.radians(45 + 90 * i)
    hole = (cq.Workplane("XY")
            .center(lug_r * math.cos(a), lug_r * math.sin(a))
            .circle(2.25).extrude(t_bot))
    bottom = bottom.cut(hole)
# re-clear the ring interior (necks must not intrude)
bottom = bottom.cut(cq.Workplane("XY").circle(R_bot_in).extrude(t_bot))

# ---------------- top motor mount ----------------
top = (cq.Workplane("XY").workplane(offset=H - t_top)
       .circle(R_top).extrude(t_top))

# ---------------- inclined struts ----------------
rb, rt = 27.5, 17.0
zb, zt = t_bot / 2.0, H - t_top / 2.0
struts = None
for i in range(n_strut):
    a = 2 * math.pi * i / n_strut
    p0 = cq.Vector(rb * math.cos(a), rb * math.sin(a), zb)
    p1 = cq.Vector(rt * math.cos(a), rt * math.sin(a), zt)
    d = p1 - p0
    cyl = cq.Solid.makeCylinder(r_strut, d.Length, p0, d.normalized())
    s = cq.Workplane("XY").add(cyl)
    struts = s if struts is None else struts.union(s)

# ---------------- mid-height reinforcement ring ----------------
r_mid = (rb + rt) / 2.0
mid_ring = (cq.Workplane("XY").workplane(offset=z_mid - 1.5)
            .circle(r_mid + 2.0).circle(r_mid - 2.0).extrude(3.0))

frame = bottom.union(top).union(struts).union(mid_ring)

# ---------------- top holes ----------------
bearing = (cq.Workplane("XY").workplane(offset=H - t_top - 1)
           .circle(5.0).extrude(t_top + 2))
motor_holes = (cq.Workplane("XY").workplane(offset=H - t_top - 1)
               .polarArray(12.0, 45, 360, 4).circle(1.5).extrude(t_top + 2))
frame = frame.cut(bearing).cut(motor_holes)

# ---------------- attempt fillets at junctions ----------------
result = frame
try:
    result = frame.edges(cq.selectors.BoxSelector((-40, -40, t_bot - 0.5),
                                                  (40, 40, t_bot + 0.5))).fillet(0.8)
except Exception:
    result = frame
try:
    result = result.edges(cq.selectors.BoxSelector((-40, -40, H - t_top - 0.5),
                                                   (40, 40, H - t_top + 0.5))).fillet(0.8)
except Exception:
    pass

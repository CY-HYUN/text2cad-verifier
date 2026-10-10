import cadquery as cq
import math

m = 3.0
z = 20
alpha = math.radians(20)
r = m * z / 2.0
rb = r * math.cos(alpha)          # 28.19
ra = r + m                        # 33.0 -> addendum radius 31.5 would be r+m=33; use standard ha=m
ra = r + m
rf = r - 1.25 * m                 # root radius
T = 15.0

def pol(rad, ang):
    return (rad * math.cos(ang), rad * math.sin(ang))

tp = math.sqrt((r / rb) ** 2 - 1)
inv_p = tp - math.atan(tp)
ta = math.sqrt((ra / rb) ** 2 - 1)
half = math.pi / (2 * z)
N = 8
pitch = 2 * math.pi / z

def flank_angle(t):
    return (t - math.atan(t)) - inv_p - half

ts = [ta * i / N for i in range(N + 1)]

wp = cq.Workplane("XY")
start = pol(rf, flank_angle(0) )
wp = wp.moveTo(*start)
corners = []
for k in range(z):
    off = k * pitch
    # right flank: root -> base -> tip
    wp = wp.lineTo(*pol(rf, flank_angle(0) + off))
    corners.append(pol(rf, flank_angle(0) + off))
    for t in ts:
        rad = rb * math.sqrt(1 + t * t)
        wp = wp.lineTo(*pol(rad, flank_angle(t) + off))
    # top land to left flank
    for t in reversed(ts):
        rad = rb * math.sqrt(1 + t * t)
        wp = wp.lineTo(*pol(rad, -flank_angle(t) + off))
    wp = wp.lineTo(*pol(rf, -flank_angle(0) + off))
    corners.append(pol(rf, -flank_angle(0) + off))
    # root arc to next tooth
    a1 = -flank_angle(0) + off
    a2 = flank_angle(0) + (k + 1) * pitch
    mid = pol(rf, (a1 + a2) / 2)
    end = pol(rf, a2)
    wp = wp.threePointArc(mid, end)

gear = wp.close().extrude(T)

try:
    def near_corner(e):
        c = e.Center()
        return any(abs(c.x - cx) < 1e-3 and abs(c.y - cy) < 1e-3 for cx, cy in corners)
    sel = [e for e in gear.edges("|Z").vals() if near_corner(e)]
    gear = cq.Workplane("XY").add(gear.val().fillet(0.9, sel))
except Exception:
    pass

# bore with keyway
bore = cq.Workplane("XY").circle(10.0).extrude(T)
key = cq.Workplane("XY").center(6.5, 0).rect(13.0, 6.0).extrude(T)
cutter = bore.union(key)

result = gear.cut(cutter)

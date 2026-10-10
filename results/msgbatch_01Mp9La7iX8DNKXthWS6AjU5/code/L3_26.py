import cadquery as cq
import math

R0, R1 = 50.0, 90.0
H = R1 - R0

def s_rise(t):
    # modified sine displacement, t in [0,1]
    return t - math.sin(2 * math.pi * t) / (2 * math.pi)

def r_main(deg):
    d = deg % 360.0
    if d < 180:
        return R0
    if d < 270:
        return R0 + H * s_rise((d - 180) / 90.0)
    return R1 - H * s_rise((d - 270) / 90.0)

def pt(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))

# main cam profile
pts_main = [pt(r_main(a), a) for a in range(180, 361, 5)]
main_sk = (cq.Workplane("XY")
           .moveTo(R0, 0)
           .threePointArc((0, R0), (-R0, 0))
           .spline(pts_main[1:], includeCurrent=True)
           .close())
main = main_sk.extrude(15.0)

# conjugate (secondary) cam: r2(theta) = 2*(R0+R1)/2 - r(theta+180)
C = R0 + R1
def r_sec(deg):
    return C - r_main(deg + 180.0)

pts_sec = [pt(r_sec(a), a) for a in range(0, 181, 5)]
sec_sk = (cq.Workplane("XY").workplane(offset=35.0)
          .moveTo(*pts_sec[0])
          .spline(pts_sec[1:], includeCurrent=True)
          .threePointArc((0, -R1), (R1, 0))
          .close())
sec = sec_sk.extrude(15.0)

# shaft hole with keyway
def cutter():
    cyl = cq.Workplane("XY").workplane(offset=-5).circle(12.5).extrude(70)
    key = (cq.Workplane("XY").workplane(offset=-5)
           .center(0, (0 + 12.5 + 6.0) / 2.0)
           .rect(6.0, 12.5 + 6.0).extrude(70))
    return cyl.union(key)

main = main.cut(cutter())
sec = sec.cut(cutter())

main = main.edges().chamfer(1.0)
sec = sec.edges().chamfer(1.0)

result = main.union(sec)

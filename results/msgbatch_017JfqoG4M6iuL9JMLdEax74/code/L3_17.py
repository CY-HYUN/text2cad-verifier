import cadquery as cq
import math

R = 25.0          # outer radius
L = 100.0         # length
A = 15.0          # sine amplitude
Y0 = 50.0         # reference axial position
Rc = 24.0         # radius of semicircle centre (depth 5 -> bottom at r=20)
rg = 4.0          # groove half-width / bottom radius

body = cq.Workplane("XY").circle(R).extrude(L)

N = 120
def curve_pts(r):
    return [
        (r * math.cos(t), r * math.sin(t), Y0 + A * math.sin(t))
        for t in [2 * math.pi * i / N for i in range(N)]
    ]

path = cq.Workplane("XY").spline(curve_pts(Rc), periodic=True, includeCurrent=False)
aux = cq.Workplane("XY").spline(curve_pts(Rc + 6.0), periodic=True, includeCurrent=False)

# Profile plane at theta=0: point (Rc,0,Y0), tangent (0,Rc,A)
tan = cq.Vector(0, Rc, A).normalized()
plane = cq.Plane(origin=(Rc, 0, Y0), xDir=(1, 0, 0), normal=tan.toTuple())

def profile():
    # local x = radial outward, local y = groove width direction
    return (
        cq.Workplane(plane)
        .moveTo(3.0, rg)
        .lineTo(0.0, rg)
        .threePointArc((-rg, 0.0), (0.0, -rg))
        .lineTo(3.0, -rg)
        .close()
    )

groove = None
try:
    groove = profile().sweep(path, auxSpine=aux)
    if groove.val().Volume() <= 0:
        raise ValueError
except Exception:
    try:
        groove = profile().sweep(path, isFrenet=True)
        if groove.val().Volume() <= 0:
            raise ValueError
    except Exception:
        # Fallback: union of ball-ended tubes approximating the U groove
        groove = None
        for rr in (Rc, Rc + 1.0, Rc + 2.0):
            p = cq.Workplane("XY").spline(curve_pts(rr), periodic=True, includeCurrent=False)
            pl = cq.Plane(origin=(rr, 0, Y0), xDir=(1, 0, 0),
                          normal=cq.Vector(0, rr, A).normalized().toTuple())
            tube = cq.Workplane(pl).circle(rg).sweep(p, isFrenet=True)
            groove = tube if groove is None else groove.union(tube)

result = body.cut(groove)

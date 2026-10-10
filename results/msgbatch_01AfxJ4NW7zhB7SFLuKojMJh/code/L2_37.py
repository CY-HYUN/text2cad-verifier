import cadquery as cq
import math

sphere = cq.Workplane("XY").sphere(20)

def make_arm():
    return cq.Workplane("XY").workplane(offset=15).circle(7.5).extrude(35)

def make_hole():
    return cq.Workplane("XY").workplane(offset=40).circle(4).extrude(10)

rots = [
    ((0,0,0),(0,0,1),0),
    ((0,0,0),(1,0,0),180),
    ((0,0,0),(0,1,0),90),
    ((0,0,0),(0,1,0),-90),
    ((0,0,0),(1,0,0),-90),
    ((0,0,0),(1,0,0),90),
]

body = sphere
for o, a, ang in rots:
    arm = make_arm()
    if ang != 0:
        arm = arm.rotate(o, a, ang)
    body = body.union(arm)

for o, a, ang in rots:
    h = make_hole()
    if ang != 0:
        h = h.rotate(o, a, ang)
    body = body.cut(h)

result = body

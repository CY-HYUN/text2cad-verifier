import cadquery as cq
import math

R = 40
T = 10

result = cq.Workplane("XY").circle(R).extrude(T)

# U-shaped slot (stadium) along +X from r=14 to r=30, width 8
def slot_at(angle):
    s = (cq.Workplane("XY")
         .center(22, 0)
         .slot2D(16, 8, 0)
         .extrude(T))
    return s.rotate((0, 0, 0), (0, 0, 1), angle)

def notch_at(angle):
    a = math.radians(angle)
    c = (cq.Workplane("XY")
         .center(R * math.cos(a), R * math.sin(a))
         .circle(20)
         .extrude(T))
    return c

for i in range(4):
    result = result.cut(slot_at(90 * i))
    result = result.cut(notch_at(45 + 90 * i))

# center hole
result = result.cut(cq.Workplane("XY").circle(5).extrude(T))

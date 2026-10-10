import cadquery as cq
import math

col_d = 20.0
col_h = 100.0
n_steps = 10
step_t = 5.0
step_ang = 30.0
step_r = 50.0
dz = 10.0

result = cq.Workplane("XY").circle(col_d / 2).extrude(col_h)

for i in range(n_steps):
    a0 = math.radians(i * step_ang)
    a1 = math.radians(i * step_ang + step_ang)
    am = (a0 + a1) / 2
    z = i * dz
    p0 = (step_r * math.cos(a0), step_r * math.sin(a0))
    pm = (step_r * math.cos(am), step_r * math.sin(am))
    p1 = (step_r * math.cos(a1), step_r * math.sin(a1))
    step = (
        cq.Workplane("XY", origin=(0, 0, z))
        .moveTo(0, 0)
        .lineTo(*p0)
        .threePointArc(pm, p1)
        .close()
        .extrude(step_t)
    )
    result = result.union(step)

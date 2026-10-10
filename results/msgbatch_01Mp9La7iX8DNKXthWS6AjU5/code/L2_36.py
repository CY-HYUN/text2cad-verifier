import cadquery as cq
import math

# Ring: OD120, ID80, thickness 20 (extruded from z=0 to z=20)
ring = (cq.Workplane("XY")
        .circle(60).circle(40)
        .extrude(20))

pcd_r = 50.0       # construction circle diameter 100
cs_d = 10.0        # countersink (counterbore-like) diameter
cs_depth = 10.0    # depth of the larger diameter
thru_d = 6.0       # through hole diameter
top = 20.0
n = 6

result = ring
for i in range(n):
    a = math.radians(i * 360.0 / n)
    x = pcd_r * math.cos(a)
    y = pcd_r * math.sin(a)
    # through hole
    thru = (cq.Workplane("XY").workplane(offset=0)
            .center(x, y).circle(thru_d / 2).extrude(top))
    # stepped large-diameter portion, 10 deep from top (revolved-cut style profile: cone-free step)
    cs = (cq.Workplane("XY").workplane(offset=top - cs_depth)
          .center(x, y).circle(cs_d / 2).extrude(cs_depth))
    result = result.cut(thru).cut(cs)

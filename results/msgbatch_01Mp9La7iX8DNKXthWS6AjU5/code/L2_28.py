import cadquery as cq

outer = cq.Workplane("XY").box(60, 60, 60)
inner = cq.Workplane("XY").box(50, 50, 50)
shell = outer.cut(inner)

core = cq.Workplane("XY").box(20, 20, 20)

d = 2.0
# pins from x=10 to x=25 (touching inner wall); extend slightly into wall for solid fusion
L = 15.5
c = 10 + L / 2 - 0.0

pin_x = cq.Workplane("YZ").workplane(offset=10).circle(d / 2).extrude(L)
pin_xn = cq.Workplane("YZ").workplane(offset=-10).circle(d / 2).extrude(-L)
pin_y = cq.Workplane("XZ").workplane(offset=-10).circle(d / 2).extrude(-L)
pin_yn = cq.Workplane("XZ").workplane(offset=10).circle(d / 2).extrude(L)
pin_z = cq.Workplane("XY").workplane(offset=10).circle(d / 2).extrude(L)
pin_zn = cq.Workplane("XY").workplane(offset=-10).circle(d / 2).extrude(-L)

result = shell.union(core)
for p in [pin_x, pin_xn, pin_y, pin_yn, pin_z, pin_zn]:
    result = result.union(p)

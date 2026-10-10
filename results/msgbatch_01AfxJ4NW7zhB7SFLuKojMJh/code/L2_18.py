import cadquery as cq

L, W, H = 100.0, 40.0, 30.0

body = cq.Workplane("XY").box(L, W, H, centered=(True, True, False))

# semicircular groove along the full length on top face
r = 10.0
cyl = (cq.Workplane("YZ").workplane(offset=-L/2)
       .center(0, H).circle(r).extrude(L))
body = body.cut(cyl)

# side lightweight grooves
gl, gh, gd = 60.0, 10.0, 5.0
zc = H/2
for s in (1, -1):
    cutter = (cq.Workplane("XY")
              .box(gl, gd, gh)
              .translate((0, s*(W/2 - gd/2), zc)))
    body = body.cut(cutter)

result = body

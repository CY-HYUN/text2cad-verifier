import cadquery as cq

# 40 mm cube, chamfer the four vertical edges by 10 mm, then cut the 30 mm through-hole.
# The chamfer is applied before the hole so that only the four cube edges are selected,
# not the seam edge of the cylindrical hole. The final shape is the same either way.
body = cq.Workplane("XY").box(40, 40, 40).edges("|Z").chamfer(10)
result = body.faces(">Z").workplane().hole(30)

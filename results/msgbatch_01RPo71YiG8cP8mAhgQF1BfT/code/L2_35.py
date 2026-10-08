import cadquery as cq

size = 60.0
r = 10.0
L = size * 2

cube = cq.Workplane("XY").box(size, size, size)


def make_cutters(ang):
    # Hole along X, axis in the plane Z = 5
    cx = cq.Solid.makeCylinder(r, L, cq.Vector(-L / 2, 0, 5), cq.Vector(1, 0, 0))
    # Rotate about its own axis so the seam edge avoids tangency points
    cx = cx.rotate(cq.Vector(0, 0, 5), cq.Vector(1, 0, 5), ang)
    # Hole along Y, axis in the plane Z = -5
    cy = cq.Solid.makeCylinder(r, L, cq.Vector(0, -L / 2, -5), cq.Vector(0, 1, 0))
    cy = cy.rotate(cq.Vector(0, 0, -5), cq.Vector(0, 1, -5), ang + 11.0)
    return cx, cy


result = None
for ang in (37.0, 23.0, 61.0, 113.0, 151.0):
    cx, cy = make_cutters(ang)
    candidate = cube.cut(cq.Workplane("XY").add(cx)).cut(cq.Workplane("XY").add(cy))
    if candidate.val().isValid():
        result = candidate
        break

if result is None:
    cx, cy = make_cutters(37.0)
    result = cube.cut(cq.Workplane("XY").add(cx)).cut(cq.Workplane("XY").add(cy)).clean()

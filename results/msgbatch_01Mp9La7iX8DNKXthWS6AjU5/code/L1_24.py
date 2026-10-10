import cadquery as cq

# Vertical plate: sketch on YZ plane (40 wide in Y, 60 high in Z), extrude 10 along +X
vertical = (
    cq.Workplane("YZ")
    .center(20, 30)
    .rect(40, 60)
    .extrude(10)
)

# Horizontal plate: sketch on XY plane (50 long in X, 40 wide in Y), extrude 10 along +Z
horizontal = (
    cq.Workplane("XY")
    .center(25, 20)
    .rect(50, 40)
    .extrude(10)
)

result = vertical.union(horizontal)

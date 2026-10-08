import cadquery as cq

L = 60.0
S = 40.0

result = cq.Workplane("XY").box(L, L, L)

# Front view cut (through Y)
result = result.cut(cq.Workplane("XZ").rect(S, S).extrude(L, both=True))
# Top view cut (through Z)
result = result.cut(cq.Workplane("XY").rect(S, S).extrude(L, both=True))
# Right view cut (through X)
result = result.cut(cq.Workplane("YZ").rect(S, S).extrude(L, both=True))

import cadquery as cq
import math

# Create the drone motor mount frame
result = cq.Workplane("XY")

# Bottom mounting ring (60mm diameter)
bottom_ring = cq.Workplane("XY").circle(30).extrude(5)

# Top motor mount (40mm diameter)
top_mount = cq.Workplane("XY").workplane(offset=80).circle(20).extrude(5)

# Create bottom ring with M4 bolt hole lugs
bottom_ring_with_lugs = cq.Workplane("XY").circle(30).extrude(5)

# Add four M4 bolt hole lugs at 90-degree intervals on bottom ring
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = 35 * math.cos(rad)
    y = 35 * math.sin(rad)
    lug = cq.Workplane("XY").center(x, y).circle(6).extrude(3)
    bottom_ring_with_lugs = bottom_ring_with_lugs.union(lug)

# Create M4 holes in lugs
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = 35 * math.cos(rad)
    y = 35 * math.sin(rad)
    hole = cq.Workplane("XY").center(x, y).circle(2).extrude(10)
    bottom_ring_with_lugs = bottom_ring_with_lugs.cut(hole)

# Cut central hole in bottom ring
bottom_ring_with_lugs = bottom_ring_with_lugs.cut(cq.Workplane("XY").circle(25).extrude(10))

# Create top mount with central bearing hole and motor fixing holes
top_mount_assembly = cq.Workplane("XY").workplane(offset=80).circle(20).extrude(5)

# Central bearing hole (10mm diameter)
top_mount_assembly = top_mount_assembly.cut(cq.Workplane("XY").workplane(offset=80).circle(5).extrude(10))

# Four motor fixing holes (3mm diameter) at 90-degree intervals
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = 12 * math.cos(rad)
    y = 12 * math.sin(rad)
    hole = cq.Workplane("XY").workplane(offset=80).center(x, y).circle(1.5).extrude(10)
    top_mount_assembly = top_mount_assembly.cut(hole)

# Create eight inclined cylindrical supports
supports = []
for i in range(8):
    angle = (i * 45) * math.pi / 180
    
    # Bottom connection point (on 60mm ring)
    x_bottom = 28 * math.cos(angle)
    y_bottom = 28 * math.sin(angle)
    
    # Top connection point (on 40mm ring)
    x_top = 18 * math.cos(angle)
    y_top = 18 * math.sin(angle)
    
    # Mid-height point (on reinforcement ring)
    x_mid = 24 * math.cos(angle)
    y_mid = 24 * math.sin(angle)
    
    # Create support rod from bottom to top
    support = cq.Workplane("XY").moveTo(x_bottom, y_bottom).lineTo(x_top, y_top).extrude(4, taper=-0.3)
    supports.append(support)

# Create horizontal reinforcement ring at mid-height (z=40)
reinforcement_ring = (cq.Workplane("XY")
                      .workplane(offset=40)
                      .circle(24)
                      .extrude(3))
reinforcement_ring = reinforcement_ring.cut(cq.Workplane("XY").workplane(offset=40).circle(22).extrude(5))

# Combine all components
result = bottom_ring_with_lugs

for support in supports:
    result = result.union(support)

result = result.union(reinforcement_ring)
result = result.union(top_mount_assembly)

# Apply fillets at connection points for smoothness
result = result.edges("|Z").fillet(1.5)


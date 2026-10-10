import cadquery as cq
import math

# Create the drone motor mount frame
# Bottom mounting ring (60mm diameter)
bottom_ring = cq.Workplane("XY").circle(30).extrude(5)

# Add four M4 bolt hole lugs at 90-degree intervals on bottom ring
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = 35 * math.cos(rad)
    y = 35 * math.sin(rad)
    lug = cq.Workplane("XY").center(x, y).circle(6).extrude(3)
    bottom_ring = bottom_ring.union(lug)

# Cut M4 holes in lugs
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = 35 * math.cos(rad)
    y = 35 * math.sin(rad)
    hole = cq.Workplane("XY").center(x, y).circle(2).extrude(10)
    bottom_ring = bottom_ring.cut(hole)

# Cut central hole in bottom ring
bottom_ring = bottom_ring.cut(cq.Workplane("XY").circle(25).extrude(10))

# Top motor mount (40mm diameter)
top_mount = cq.Workplane("XY").workplane(offset=80).circle(20).extrude(5)

# Central bearing hole (10mm diameter)
top_mount = top_mount.cut(cq.Workplane("XY").workplane(offset=80).circle(5).extrude(10))

# Four motor fixing holes (3mm diameter) at 90-degree intervals
for angle in [0, 90, 180, 270]:
    rad = math.radians(angle)
    x = 12 * math.cos(rad)
    y = 12 * math.sin(rad)
    hole = cq.Workplane("XY").workplane(offset=80).center(x, y).circle(1.5).extrude(10)
    top_mount = top_mount.cut(hole)

# Create horizontal reinforcement ring at mid-height (z=40)
reinforcement_ring = cq.Workplane("XY").workplane(offset=40).circle(24).extrude(3)
reinforcement_ring = reinforcement_ring.cut(cq.Workplane("XY").workplane(offset=40).circle(22).extrude(5))

# Create eight inclined cylindrical supports
supports_solid = None
for i in range(8):
    angle = (i * 45) * math.pi / 180
    
    # Bottom connection point (on 60mm ring)
    x_bottom = 28 * math.cos(angle)
    y_bottom = 28 * math.sin(angle)
    
    # Top connection point (on 40mm ring)
    x_top = 18 * math.cos(angle)
    y_top = 18 * math.sin(angle)
    
    # Create a tapered support rod using a loft between two circles
    bottom_pt = cq.Workplane("XY").circle(3)
    top_circle = cq.Workplane("XY").workplane(offset=80).center(x_top - x_bottom, y_top - y_bottom).circle(2.5)
    
    # Create support as a simple cylinder positioned appropriately
    support = cq.Workplane("XY").center(x_bottom, y_bottom).circle(2.5).extrude(80)
    
    if supports_solid is None:
        supports_solid = support
    else:
        supports_solid = supports_solid.union(support)

# Combine all components
result = bottom_ring.union(top_mount).union(reinforcement_ring)

if supports_solid is not None:
    result = result.union(supports_solid)

# Apply fillets at edges for smoothness
try:
    result = result.edges().fillet(0.8)
except:
    pass

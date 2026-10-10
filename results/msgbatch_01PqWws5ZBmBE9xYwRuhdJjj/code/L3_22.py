import cadquery as cq
import math

# Initialize the base
result = cq.Workplane("XY")

# Base sketch - annular ring with 4 lugs and M4 bolt holes
base_sketch = (
    cq.Sketch()
    .circle(30)  # Outer radius 30mm (diameter 60mm)
    .circle(20)  # Inner radius 20mm
    .vertices()
    .circle(2.5)  # M4 bolt holes (2mm radius for M4)
)

# Create annular ring
base = result.placeSketch(base_sketch).extrude(5)

# Add four lugs with M4 holes at 90-degree intervals
lug_positions = [0, 90, 180, 270]
for angle in lug_positions:
    angle_rad = math.radians(angle)
    x = 32 * math.cos(angle_rad)
    y = 32 * math.sin(angle_rad)
    
    # Create lug sketch at offset position
    lug_sketch = cq.Sketch().circle(6).circle(2)  # Lug body with M4 hole
    lug = cq.Workplane("XY").placeSketch(lug_sketch).extrude(5)
    lug = lug.translate((x, y, 0))
    base = base.union(lug)

# Top motor mount at height 25mm
top_mount = cq.Workplane("XY").transformed(offset=(0, 0, 25))

# Motor mount sketch - 40mm diameter with 10mm bearing hole and 4 M3 holes
motor_sketch = (
    cq.Sketch()
    .circle(20)  # 40mm diameter
    .circle(5)   # 10mm bearing hole
)

# Add 4 motor mounting holes around center (at 16mm radius, 90-degree intervals)
for i in range(4):
    angle = i * 90
    angle_rad = math.radians(angle)
    mx = 16 * math.cos(angle_rad)
    my = 16 * math.sin(angle_rad)
    motor_sketch = motor_sketch.circle(1.5, (mx, my))  # 3mm diameter holes

top_mount_solid = top_mount.placeSketch(motor_sketch).extrude(3)

# Create 8 inclined cylindrical pillars
pillar_height = 25
num_pillars = 8
pillar_radius = 3

pillars = []
for i in range(num_pillars):
    angle = i * (360 / num_pillars)
    angle_rad = math.radians(angle)
    
    # Base position at radius 28mm
    base_x = 28 * math.cos(angle_rad)
    base_y = 28 * math.sin(angle_rad)
    
    # Top position at radius 16mm (inclined toward center)
    top_x = 16 * math.cos(angle_rad)
    top_y = 16 * math.sin(angle_rad)
    
    # Create pillar as a tapered cylinder
    pillar = (
        cq.Workplane("XY")
        .circle(pillar_radius)
        .extrude(pillar_height)
        .translate((base_x, base_y, 5))
    )
    
    # Taper the pillar (create frustum effect)
    top_face = pillar.faces(">Z").val()
    pillar = pillar.workplane(offset=pillar_height).circle(2.5).cutThruAll()
    
    pillars.append(pillar)

# Combine all pillars
pillar_assembly = pillars[0]
for pillar in pillars[1:]:
    pillar_assembly = pillar_assembly.union(pillar)

# Create intermediate reinforcing ring at mid-height (height 17.5mm)
ring_sketch = cq.Sketch().circle(22).circle(14)  # Reinforcing ring
reinforcing_ring = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 17.5))
    .placeSketch(ring_sketch)
    .extrude(2)
)

# Combine all components
result = base.union(pillar_assembly).union(reinforcing_ring).union(top_mount_solid)

# Apply fillets to all edges for stress distribution
edges_to_fillet = result.edges()
result = result.fillet(2.5)  # Large radius fillets on all edges

# Ensure proper merging and final shape
result = result.consolidate()

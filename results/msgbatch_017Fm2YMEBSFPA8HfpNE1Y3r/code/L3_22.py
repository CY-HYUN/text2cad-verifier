import cadquery as cq
import math

# Initialize the base workplane
base = cq.Workplane("XY")

# Create base annular ring with outer diameter 60mm
base_ring = base.circle(30).circle(20).extrude(5)

# Add four lugs with M4 bolt holes at 90-degree intervals
lug_radius = 32
for i in range(4):
    angle = i * 90
    angle_rad = math.radians(angle)
    x = lug_radius * math.cos(angle_rad)
    y = lug_radius * math.sin(angle_rad)
    
    lug = cq.Workplane("XY").circle(6).extrude(5).translate((x, y, 0))
    lug = lug.circle(2).cutThruAll()
    base_ring = base_ring.union(lug)

# Create top motor mount at height 25mm
top_mount_plane = cq.Workplane("XY").transformed(offset=(0, 0, 25))
top_mount = top_mount_plane.circle(20).extrude(3)

# Add bearing hole (10mm diameter = 5mm radius)
top_mount = top_mount.circle(5).cutThruAll()

# Add four M3 mounting holes (3mm diameter = 1.5mm radius) at 16mm radius
motor_hole_radius = 16
for i in range(4):
    angle = i * 90
    angle_rad = math.radians(angle)
    mx = motor_hole_radius * math.cos(angle_rad)
    my = motor_hole_radius * math.sin(angle_rad)
    hole = cq.Workplane("XY").circle(1.5).extrude(10)
    hole = hole.translate((mx, my, 20))
    top_mount = top_mount.union(hole)
    top_mount = top_mount.circle(1.5, (mx, my)).cutThruAll()

# Create 8 inclined cylindrical pillars
pillar_height = 20
num_pillars = 8
pillar_radius = 3.0
base_radius = 28
top_radius = 16

pillars_combined = None
for i in range(num_pillars):
    angle = i * (360.0 / num_pillars)
    angle_rad = math.radians(angle)
    
    # Base position at radius 28mm
    base_x = base_radius * math.cos(angle_rad)
    base_y = base_radius * math.sin(angle_rad)
    
    # Create pillar as a cylinder
    pillar = cq.Workplane("XY").circle(pillar_radius).extrude(pillar_height)
    pillar = pillar.translate((base_x, base_y, 5))
    
    if pillars_combined is None:
        pillars_combined = pillar
    else:
        pillars_combined = pillars_combined.union(pillar)

# Create intermediate reinforcing ring at mid-height (height 17.5mm)
ring_plane = cq.Workplane("XY").transformed(offset=(0, 0, 17.5))
reinforcing_ring = ring_plane.circle(22).circle(14).extrude(2)

# Combine all components
result = base_ring.union(pillars_combined).union(reinforcing_ring).union(top_mount)

# Apply fillets to edges for smooth stress distribution
result = result.fillet(1.5)


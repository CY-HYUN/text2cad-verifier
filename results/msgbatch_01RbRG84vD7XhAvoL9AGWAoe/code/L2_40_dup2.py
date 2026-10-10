import cadquery as cq
import math

# Parameters
D = 30.0
R = D / 2.0
L = 60.0
depth = 1.0
spacing = 2.0
helix_angle = 45.0

# Number of grooves around circumference (one set)
N = int(round(math.pi * D / spacing))  # ~47

# Star-shaped cross-section: V-grooves of given depth
pts = []
for i in range(N):
    a0 = 2 * math.pi * i / N
    a1 = 2 * math.pi * (i + 0.5) / N
    pts.append((R * math.cos(a0), R * math.sin(a0)))
    pts.append(((R - depth) * math.cos(a1), (R - depth) * math.sin(a1)))

# Twist angle for a 45-degree helix over the length:
# tan(45) = (R * dtheta) / dz  -> dtheta = L * tan(angle) / R
twist_deg = math.degrees(L * math.tan(math.radians(helix_angle)) / R)

right_hand = (
    cq.Workplane("XY")
    .polyline(pts).close()
    .twistExtrude(L, twist_deg)
)

left_hand = (
    cq.Workplane("XY")
    .polyline(pts).close()
    .twistExtrude(L, -twist_deg)
)

# Intersection of the two helical groove sets -> rhombic pyramid knurl
result = right_hand.intersect(left_hand)

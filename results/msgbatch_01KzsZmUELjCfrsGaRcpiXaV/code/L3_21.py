import cadquery as cq
import math

# Create the Laval Nozzle as an axisymmetric body of revolution

# Parameters
inlet_flange_dia = 60
outlet_flange_dia = 60
flange_thickness = 5
convergent_length = 20
divergent_length = 80
total_length = convergent_length + divergent_length
throat_diameter = 10
throat_radius = throat_diameter / 2
exit_diameter = 40
exit_radius = exit_diameter / 2
inlet_arc_radius = 50
max_outer_diameter = 60
max_outer_radius = max_outer_diameter / 2

# Create a 2D profile that will be revolved around the axis
profile_points = []

# Start at inlet flange outer edge
profile_points.append((max_outer_radius, 0))
profile_points.append((inlet_flange_dia/2, 0))
profile_points.append((inlet_flange_dia/2, flange_thickness))

# Inlet curved section with arc
# Arc connects from inlet radius at z=flange_thickness to throat_radius at z=convergent_length
arc_center_x = inlet_flange_dia/2 - inlet_arc_radius
arc_center_z = flange_thickness

angle_start = math.atan2(flange_thickness - arc_center_z, inlet_flange_dia/2 - arc_center_x)
angle_end = math.atan2(convergent_length - arc_center_z, throat_radius - arc_center_x)

for i in range(21):
    t = i / 20.0
    angle = angle_start + (angle_end - angle_start) * t
    x = arc_center_x + inlet_arc_radius * math.cos(angle)
    z = arc_center_z + inlet_arc_radius * math.sin(angle)
    if x > throat_radius * 0.99:
        profile_points.append((x, z))

# Throat
profile_points.append((throat_radius, convergent_length))

# Divergent section with parabolic expansion
a = (exit_radius - throat_radius) / (divergent_length ** 2)

for i in range(1, 81):
    z_offset = i
    z = convergent_length + z_offset
    r = a * (z_offset ** 2) + throat_radius
    profile_points.append((r, z))

# Exit
profile_points.append((exit_radius, total_length))

# Outlet flange
profile_points.append((outlet_flange_dia/2, total_length))
profile_points.append((outlet_flange_dia/2, total_length + flange_thickness))

# Outer wall (back side)
profile_points.append((max_outer_radius, total_length + flange_thickness))
profile_points.append((max_outer_radius, total_length))

# Outer structural contour
for i in range(100, 0, -1):
    t = i / 100.0
    z = total_length - t * total_length
    r = max_outer_radius - (max_outer_radius - outlet_flange_dia/2) * (1 - t)
    profile_points.append((r, z))

profile_points.append((max_outer_radius, flange_thickness))
profile_points.append((max_outer_radius, 0))

# Create sketch using Wire with Line segments
plane = cq.Workplane("XZ")
pts_2d = [(p[0], p[1]) for p in profile_points]

# Use spline or polyline to create the profile
wire = cq.Wire.makePolygon([(p[0], 0, p[1]) for p in profile_points], forceClose=True)

# Create face from wire
face = cq.Face.makeFromWires(wire)

# Revolve around Z axis
result = cq.Workplane("XY").workplane(offset=0).sweep(face, path=None, makeSolid=True)

# Alternative approach: use revolve with Wire directly
axis = cq.Vector(0, 0, 1)
origin = cq.Vector(0, 0, 0)

result = cq.Workplane("XZ").polyline(pts_2d).close().revolve(360, axis=axis)

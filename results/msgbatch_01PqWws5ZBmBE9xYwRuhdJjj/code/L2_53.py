import cadquery as cq
import math

# Create the base cube
cube_size = 60
cube = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# Define the circle diameter for cutting
circle_diameter = 40
circle_radius = circle_diameter / 2

# Cut circles through each face of the cube
# Front face (XY plane, Z = 30)
cube = cube.faces("+Z").workplane().hole(circle_diameter, cube_size + 10)
# Back face (XY plane, Z = -30)
cube = cube.faces("-Z").workplane().hole(circle_diameter, cube_size + 10)

# Top face (XZ plane, Y = 30)
cube = cube.faces("+Y").workplane().hole(circle_diameter, cube_size + 10)
# Bottom face (XZ plane, Y = -30)
cube = cube.faces("-Y").workplane().hole(circle_diameter, cube_size + 10)

# Right face (YZ plane, X = 30)
cube = cube.faces("+X").workplane().hole(circle_diameter, cube_size + 10)
# Left face (YZ plane, X = -30)
cube = cube.faces("-X").workplane().hole(circle_diameter, cube_size + 10)

# Create the sphere at the center with diameter 30mm
sphere_diameter = 30
sphere_radius = sphere_diameter / 2
sphere = cq.Workplane("XY").sphere(sphere_radius)

# Create small connecting columns between sphere and inner corners of the frame
# The inner frame has corners where the circles intersect
# Calculate the corner positions of the frame cutouts
# For a cube with circles of radius 20mm cut on each face
frame_corner_distance = circle_radius / math.sqrt(2)  # Distance from center to corner of circular hole

# Create connecting cylinders from sphere to frame corners
connector_radius = 2
connector_height = frame_corner_distance

# Define 8 corners of the cube and create connectors
corners = [
    (frame_corner_distance, frame_corner_distance, frame_corner_distance),
    (frame_corner_distance, frame_corner_distance, -frame_corner_distance),
    (frame_corner_distance, -frame_corner_distance, frame_corner_distance),
    (frame_corner_distance, -frame_corner_distance, -frame_corner_distance),
    (-frame_corner_distance, frame_corner_distance, frame_corner_distance),
    (-frame_corner_distance, frame_corner_distance, -frame_corner_distance),
    (-frame_corner_distance, -frame_corner_distance, frame_corner_distance),
    (-frame_corner_distance, -frame_corner_distance, -frame_corner_distance),
]

connectors = None
for corner in corners:
    connector = cq.Workplane("XY").moveTo(0, 0).cylinder(
        height=math.sqrt(corner[0]**2 + corner[1]**2 + corner[2]**2),
        radius=connector_radius,
        centered=True
    )
    # Rotate and position connector
    x, y, z = corner
    length = math.sqrt(x**2 + y**2 + z**2)
    # Create connector from origin to corner
    connector = cq.Workplane("XY").box(connector_radius*2, connector_radius*2, length).translate((x/2, y/2, z/2))
    
    if connectors is None:
        connectors = connector
    else:
        connectors = connectors.union(connector)

# Combine all parts
result = cube.union(sphere).union(connectors)

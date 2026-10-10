import cadquery as cq
import math

# Create the base: cylinder with diameter 120mm, height 10mm
base = cq.Workplane("XY").circle(60).extrude(10)

# Create a helical centerline using parametric equations
# X(t) = (5 + 3t) * cos(t)
# Y(t) = (5 + 3t) * sin(t)
# t ranges from 0 to 3π

def helical_curve(t_max=3*math.pi, num_points=300):
    points = []
    for i in range(num_points + 1):
        t = i * (t_max / num_points)
        r = 5 + 3 * t
        x = r * math.cos(t)
        y = r * math.sin(t)
        points.append((x, y))
    return points

# Generate the centerline points
centerline_points = helical_curve()

# Create offset spirals for the groove (2mm on each side = 4mm total width)
def offset_spiral_points(points, offset_distance):
    offset_points_left = []
    offset_points_right = []
    
    for i in range(len(points)):
        x, y = points[i]
        
        # Calculate perpendicular direction (normal to the curve)
        if i == 0:
            dx = points[1][0] - points[0][0]
            dy = points[1][1] - points[0][1]
        elif i == len(points) - 1:
            dx = points[i][0] - points[i-1][0]
            dy = points[i][1] - points[i-1][1]
        else:
            dx = points[i+1][0] - points[i-1][0]
            dy = points[i+1][1] - points[i-1][1]
        
        # Normalize
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
        
        # Perpendicular (rotate 90 degrees)
        px = -dy
        py = dx
        
        offset_points_left.append((x + px * offset_distance, y + py * offset_distance))
        offset_points_right.append((x - px * offset_distance, y - py * offset_distance))
    
    return offset_points_left, offset_points_right

offset_left, offset_right = offset_spiral_points(centerline_points, 2.0)

# Create edges for the groove boundaries
edge_left = cq.Edge.makeSpline([cq.Vector(x, y, 0) for x, y in offset_left])
edge_right = cq.Edge.makeSpline([cq.Vector(x, y, 0) for x, y in offset_right])

# Close the spiral groove with lines at start and end
start_left = cq.Vector(offset_left[0][0], offset_left[0][1], 0)
start_right = cq.Vector(offset_right[0][0], offset_right[0][1], 0)
end_left = cq.Vector(offset_left[-1][0], offset_left[-1][1], 0)
end_right = cq.Vector(offset_right[-1][0], offset_right[-1][1], 0)

# Create closing lines
arc_start = cq.Edge.makeLine(start_left, start_right)
arc_end = cq.Edge.makeLine(end_right, end_left)

# Create a wire from the edges - reverse offset_right by creating new spline in opposite direction
offset_right_reversed = list(reversed(offset_right))
edge_right_rev = cq.Edge.makeSpline([cq.Vector(x, y, 0) for x, y in offset_right_reversed])

# Assemble wire from edges
wire = cq.Wire.assembleEdges([edge_left, arc_end, edge_right_rev, arc_start])

# Create face from wire
face = cq.Face.makeFromWires(wire)

# Extrude the groove 25mm downward (negative Z direction, from top surface)
groove = face.extrude(cq.Vector(0, 0, -25))

# Cut the groove from the base
result = base.cut(groove)

# Create and cut the center exhaust port (8mm diameter circle at origin)
exhaust_hole = cq.Workplane("XY").circle(4).extrude(-10)
result = result.cut(exhaust_hole)

# Apply R0.5 chamfer to top edges
result = result.edges(">Z").chamfer(0.5)

import cadquery as cq
import math

# Create a sphere with radius 30 mm
sphere = cq.Solid.makeSphere(30)

# Create a box to cut the top portion of the sphere
# The sphere center is at origin (0, 0, 0)
# We want to cut at Z = 15 mm
# The box needs to be large enough to completely cut through the top portion
# Box dimensions: large X and Y (to cover the sphere), and positioned above Z = 15

cut_box = cq.Solid.makeBox(
    length=100,  # Large enough to cover sphere in X direction
    width=100,   # Large enough to cover sphere in Y direction
    height=50,   # Height of cutting box
    pnt=cq.Vector(-50, -50, 15)  # Position so it cuts at Z = 15 and extends upward
)

# Perform the cut: sphere - cut_box
result = sphere.cut(cut_box)

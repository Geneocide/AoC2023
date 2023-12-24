from z3 import Reals, Solver, sat
from pathlib import Path


filepath = Path(__file__).parent / "input.txt"
vectors = []

with open(filepath, "r") as file:
    for line in file:
        point, velocity = line.strip().split(" @ ")
        point = tuple(int(c) for c in point.split(", "))
        velocity = tuple(int(c) for c in velocity.split(", "))
        vectors.append((point, velocity))

(x_1, y_1, z_1), (dx_1, dy_1, dz_1) = vectors[0]
(x_2, y_2, z_2), (dx_2, dy_2, dz_2) = vectors[1]
(x_3, y_3, z_3), (dx_3, dy_3, dz_3) = vectors[2]

x, y, z = Reals("x y z")
dx, dy, dz = Reals("dx dy dz")
t1, t2, t3 = Reals("t1 t2 t3")
solver = Solver()

eq1 = x + t1 * dx == x_1 + t1 * dx_1
eq2 = y + t1 * dy == y_1 + t1 * dy_1
eq3 = z + t1 * dz == z_1 + t1 * dz_1
eq4 = x + t2 * dx == x_2 + t2 * dx_2
eq5 = y + t2 * dy == y_2 + t2 * dy_2
eq6 = z + t2 * dz == z_2 + t2 * dz_2
eq7 = x + t3 * dx == x_3 + t3 * dx_3
eq8 = y + t3 * dy == y_3 + t3 * dy_3
eq9 = z + t3 * dz == z_3 + t3 * dz_3

solver.add(eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9)

if solver.check() == sat:
    model = solver.model()
    coordinateSum = sum(model[var].as_long() for var in [x, y, z])


print(
    f"What do you get if you add up the X, Y, and Z coordinates of that initial position? Answer: {coordinateSum}"
)  # answer 1016365642179116

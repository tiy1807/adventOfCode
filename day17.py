input = "target area: x=155..215, y=-132..-72"

target_area = {"x_min": 155, "x_max": 215, "y_min": -132, "y_max": -72}

initial_velocity = {"x": 19, "y": 6}

class Projectile:
    def __init__(self, initial_velocity):
        self.v_x = initial_velocity["x"]
        self.v_y = initial_velocity["y"]
        self.s_x = 0
        self.s_y = 0

    def step(self):
        self.s_x += self.v_x
        self.s_y += self.v_y
        if self.v_x > 0:
            self.v_x -= 1
        elif self.v_x < 0:
            self.v_x += 1
        self.v_y -= 1

    def generate_path(self):
        self.path = []
        while self.s_x <= target_area["x_max"] and self.s_y >= target_area["y_min"]:
            self.path.append({"x": self.s_x, "y": self.s_y})
            self.step()

    def is_in_target_area(self):
        return bool([p for p in self.path if (target_area["x_min"] <= p["x"] <= target_area["x_max"]) and (target_area["y_min"] <= p["y"] <= target_area["y_max"])])

    def max_height(self):
        return max([p["y"] for p in self.path])

count = 0
for initial_x in range(18, 216):
    initial_velocity["x"] = initial_x
    for initial_y in range(-132, 133):
        initial_velocity["y"] = initial_y
        p = Projectile(initial_velocity)
        p.generate_path()
        if p.is_in_target_area():
            count += 1
print(count)
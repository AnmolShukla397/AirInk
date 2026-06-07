class Smoother:
    def __init__(self, alpha=0.65):
        self.alpha = alpha
        self.prev = None

    def smooth(self, point):
        if self.prev is None:
            self.prev = point
            return point
        x = int(self.alpha * self.prev[0] + (1 - self.alpha) * point[0])
        y = int(self.alpha * self.prev[1] + (1 - self.alpha) * point[1])
        self.prev = (x, y)
        return self.prev

    def reset(self):
        self.prev = None
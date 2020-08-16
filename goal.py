class Goal():
    def __init__(self, balls=[]):
        self.balls = balls

    def getOwner(self):
        if self.balls:
            return self.balls[0]
        else:
            return None

    def getPoints(self, color):
        num = 0
        for ball in self.balls:
            if ball == color:
                num += 1
        return num

    def addBall(self, color):
        if len(self.balls) == 3:
            raise IndexError("Goal is full")
        self.balls.insert(0, color)

    def subtractBall(self):
        if not self.balls:
            raise IndexError("Goal is empty")
        return self.balls.pop()


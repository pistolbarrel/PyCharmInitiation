from goal import Goal


class Row:
    def __init__(self, goals=[]):
        if len(goals) >= 4 or len(goals) < 3:
            raise IndexError("Must have 3 and only 3 goals defined.")
        for goal in goals:
            if type(goal) is not Goal:
                raise TypeError("Goal types only.")
        self.goals = goals

    def getOwner(self):
        owns0 = self.goals[0].getOwner()
        if owns0 == self.goals[1].getOwner() == self.goals[2].getOwner():
            return owns0
        else:
            return None

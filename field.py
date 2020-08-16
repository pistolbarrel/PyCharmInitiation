from row import Row
from goal import Goal

def printScore():
    print("{} score {} = {} + {}, {} score {} = {} + {}".format('BLUE', f.getGoalPoints('blue') + f.getRowPoints('blue'),
          f.getGoalPoints('blue'), f.getRowPoints('blue'),'RED', f.getGoalPoints('red') + f.getRowPoints('red'),
          f.getGoalPoints('red'), f.getRowPoints('red')))

class Field:
    goals = []
    rows = []

    def __init__(self, type):
        if type == "skills":
            self.goals.append(Goal(['blue', 'blue']))
            self.goals.append(Goal(['blue']))
            self.goals.append(Goal(['blue', 'blue']))
            self.goals.append(Goal(['blue']))
            self.goals.append(Goal(['blue', 'blue', 'blue']))
            self.goals.append(Goal(['blue']))
            self.goals.append(Goal(['blue', 'blue']))
            self.goals.append(Goal(['blue']))
            self.goals.append(Goal(['blue', 'blue']))

        self.rows.append(Row([self.goals[0], self.goals[1], self.goals[2]]))
        self.rows.append(Row([self.goals[3], self.goals[4], self.goals[5]]))
        self.rows.append(Row([self.goals[6], self.goals[7], self.goals[8]]))
        self.rows.append(Row([self.goals[0], self.goals[3], self.goals[6]]))
        self.rows.append(Row([self.goals[1], self.goals[4], self.goals[7]]))
        self.rows.append(Row([self.goals[2], self.goals[5], self.goals[8]]))
        self.rows.append(Row([self.goals[0], self.goals[4], self.goals[8]]))
        self.rows.append(Row([self.goals[2], self.goals[4], self.goals[6]]))

    def getGoalPoints(self, color):
        score = 0
        for goal in self.goals:
            score += goal.getPoints(color)
        return score

    def getRowPoints(self, color):
        score = 0
        for row in self.rows:
            if row.getOwner() == color:
                score += 6
        return score

    def addBall(self, goalNum, color):
        self.goals[goalNum].addBall(color)

    def subtractBall(self, goalNum):
        self.goals[goalNum].subtractBall()

    def getOneCharOwner(self, goal):
        own = goal.getOwner()
        if own:
            if own == 'blue':
                return "b"
            else:
                return "r"
        else:
            return "X"

    def displayField(self):
        outStr = ""
        idx = 0
        for goal in self.goals:
            if not idx % 3:
                outStr += "\n"
            idx += 1
            outStr += self.getOneCharOwner(goal) + " "
        print(outStr)
        print()

f = Field("skills")
printScore()
f.displayField()
f.addBall(0, 'red')
printScore()
f.displayField()
# f.addBall(0, 'blue')
# print(f.getGoalPoints('blue'))
# print(f.getRowPoints('blue'))
f.subtractBall(0)
f.addBall(0, 'blue')
printScore()
f.displayField()


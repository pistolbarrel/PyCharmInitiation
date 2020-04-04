from graphics import *
from pip._vendor.distlib.compat import raw_input


def main():
    win = GraphWin

    print("This program plots the growth of a 10 year investment.")

    principle = float(input("Enter the initial principle "))
    apr = float(input("Enter the annualized interest rates "))/100

    win = drawChartSkeleton()
    drawPrincipleOnlyBar(principle, win)
    drawYearlyGainBars(apr, principle, win)

    raw_input("Press <Enter> to quit.")
    win.close()


def drawChartSkeleton():
    win = GraphWin("Investment Growth Chart")
    win.setBackground("white")
    win.setCoords(-1.75, -200, 11.5, 10400)
    Text(Point(-1, 0), ' 0.0K').draw(win)
    Text(Point(-1, 2500), ' 2.5K').draw(win)
    Text(Point(-1, 5000), ' 5.0K').draw(win)
    Text(Point(-1, 7500), ' 7.5K').draw(win)
    Text(Point(-1, 10000), '10.0K').draw(win)
    return win


def drawPrincipleOnlyBar(principle, win):
    bar = Rectangle(Point(0, 0), Point(1, principle))
    bar.setFill("green")
    bar.setWidth(2)
    bar.draw(win)
    return bar


def drawYearlyGainBars(apr, principle, win):
    for year in range(1, 11):
        principle = principle * (1 + apr)
        print(principle)
        bar = Rectangle(Point(year, 0), Point(year + 1, principle))
        bar.setFill("green")
        bar.setWidth(2)
        bar.draw(win)


main()


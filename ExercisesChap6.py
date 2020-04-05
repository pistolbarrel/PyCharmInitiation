import sys
from math import floor, sqrt


def main():
    label("turn_clockwise() Tests")
    test(turn_clockwise("N") == "E")
    test(turn_clockwise("W") == "N")
    test(turn_clockwise("22") is None)
    print()

    label("day_name() Tests")
    test(day_name(3) == "Wednesday")
    test(day_name(0) == "Sunday")
    test(day_name(7) is None)
    test(day_name(-1) is None)
    print()

    label("day_num() Tests")
    test(day_num("Wednesday") == 3)
    test(day_num("Sunday") == 0)
    test(day_num("Everyday") is None)
    test(day_num("Tomorrowday") is None)
    print()

    label("day_add() Tests")
    test(day_add("Monday", 4) == "Friday")
    test(day_add("Tuesday", 0) == "Tuesday")
    test(day_add("Tuesday", 14) == "Tuesday")
    test(day_add("Sunday", 100) == "Tuesday")
    test(day_add("Sunday", -1) == "Saturday")
    test(day_add("Sunday", -7) == "Sunday")
    test(day_add("Tuesday", -100) == "Sunday")
    print()

    label("days_in_month() Tests")
    test(days_in_month("FEB") == 28)
    test(days_in_month("DEC") == 31)
    test(days_in_month("Whatup") is None)
    print()

    label("to_secs() Tests")
    test(to_secs(2, 30, 10) == 9010)
    test(to_secs(2, 0, 0) == 7200)
    test(to_secs(0, 2, 0) == 120)
    test(to_secs(0, 0, 42) == 42)
    test(to_secs(0, -10, 10) == -590)
    test(to_secs(2.5, 0, 10.71) == 9010)
    test(to_secs(2.433, 0, 0) == 8758)
    print()

    label("inverse to_secs() Tests")
    test(hours_in(9010) == 2)
    test(minutes_in(9010) == 30)
    test(seconds_in(9010) == 10)
    print()

    label("compare() Tests")
    test(compare(5, 4) == 1)
    test(compare(7, 7) == 0)
    test(compare(2, 3) == -1)
    test(compare(42, 1) == 1)
    print()

    label("hypotenuse() Tests")
    test(hypotenuse(3, 4) == 5.0)
    test(hypotenuse(12, 5) == 13.0)
    test(hypotenuse(24, 7) == 25.0)
    test(hypotenuse(9, 12) == 15.0)
    print()

    label("slope() Tests")
    test(slope(5, 3, 4, 2) == 1.0)
    test(slope(1, 2, 3, 2) == 0.0)
    test(slope(1, 2, 3, 3) == 0.5)
    test(slope(2, 4, 1, 2) == 2.0)
    print()


def slope(x1, y1, x2, y2):
    return float(y2-y1) / float(x2-x1)


def hypotenuse(a, b):
    return sqrt(a**2 + b**2)

def compare(a, b):
    if a > b:
        return 1
    elif a == b:
        return 0
    return -1

def hours_in(secs):
    return int(secs / (60 * 60))


def minutes_in(secs):
    remove_whole_hours = secs % (60 * 60)
    return int(remove_whole_hours / 60)


def seconds_in(secs):
    remove_whole_hours = secs % (60 * 60)
    remove_whole_minutes = remove_whole_hours % 60
    return int(remove_whole_minutes)


def to_secs(hours, mins, secs):
    ret = hours * 60 * 60
    ret += mins * 60
    ret += secs
    return floor(ret)


def days_in_month(month):
    dim = {"JAN": 31, "FEB": 28, "MAR": 31, "APR": 30, "MAY": 31, "JUN": 30, "JUL": 31, "AUG": 31, "SEP": 30,
           "OCT": 31, "NOV": 30, "DEC": 31}
    if month in dim.keys():
        return dim[month]
    else:
        return None


def day_add(start_day_name, delta_days):
    day_delta = (day_num(start_day_name) + delta_days) % 7
    return day_name(day_delta)


def day_num(day_name):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    try:
        return days.index(day_name)
    except ValueError:
        return None


def day_name(index):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    if 0 <= index <= 6:
        return days[index]
    else:
        return None


def turn_clockwise(from_dir):
    dirs = {"N": "E", "E": "S", "S": "W", "W": "N"}
    if from_dir in dirs.keys():
        return dirs[from_dir]
    else:
        return None


def test(did_pass):
    """  Print the result of a test.  """
    linenum = sys._getframe(1).f_lineno  # Get the caller's line number.
    if did_pass:
        msg = "Test at line {0} ok.".format(linenum)
    else:
        msg = ("Test at line {0} FAILED.".format(linenum))
    print(msg)


def label(test_label):
    linenum = sys._getframe(1).f_lineno  # Get the caller's line number.
    print(test_label + " at line {0}".format(linenum))


main()

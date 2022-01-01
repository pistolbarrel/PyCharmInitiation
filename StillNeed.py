import argparse
import re


def main():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("fname", help="File in Criterion directory to check")
    args = parser.parse_args()
    if args.fname:
        filename = args.fname
    else:
        exit()

    regex = r"(\+){10,}\n(.*\n){3,8}(\+){54}\n$"
    with open(filename) as file:
        data = file.read()

    matches = re.finditer(regex, data, re.MULTILINE)

    print("Still haven't seen from '{fname}' :".format(fname=filename))
    print()

    for matchNum, match in enumerate(matches, start=1):

        print("{match}".format(match=match.group()))
        print()


        # for groupNum in range(0, len(match.groups())):
        #     groupNum = groupNum + 1
        #
        #     print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
        #                                                                     start=match.start(groupNum),
        #                                                                     end=match.end(groupNum),
        #                                                                     group=match.group(groupNum)))


if __name__ == "__main__":
    main()

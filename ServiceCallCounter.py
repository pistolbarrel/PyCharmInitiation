
def main():
    str = " one, red; one, red; one, red; one, yello; one, yello; one, yello; one, yello; one, blue; " \
          "two, red; two, red; two, red; two, red; two, red; three, yello"

    entries = str.split(';')

    comp_letter = ''
    comp_number = ''
    letter_count = 0
    number_count = 0
    with open("DataFiles/ServiceCallIP.txt", 'r') as f:
        lines = f.readlines()
    for line in lines:
        letter, number = line.split()
        # letter, number = entry.split(',')
        if not comp_number and not comp_letter:
            comp_number = number
            number_count = 0
            comp_letter = letter
            letter_count = 0
            continue
        if letter == comp_letter:
            letter_count += 1
        else:
            letter_count += 1
            number_count += 1
            print(comp_letter + " " + comp_number + " ", number_count)
            print(comp_letter + " ", letter_count)
            comp_letter = letter
            letter_count = 0
            comp_number = number
            number_count = 0
            continue
        if number == comp_number:
            number_count += 1
        else:
            number_count += 1
            print(comp_letter + " " + comp_number + " ", number_count)
            comp_number = number
            number_count = 0
    letter_count += 1
    number_count += 1
    print(comp_letter + " " + comp_number + " ", number_count)
    print(comp_letter + " ", letter_count)

    with open("DataFiles/ServiceCallIP.txt", 'r') as f:
        ln = f.readline()
        one, two = ln.split()
        a = 42


if __name__ == "__main__":
    main()
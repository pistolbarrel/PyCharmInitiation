def main():
    in_string = "OE|SWIM|542310205|retail|542310205.1|2021-05-14 08:59:01:045||A|100.0000|130.780000|B|||||||" \
                "|||||NITE|E|||N|||||||N|SWIM|||||L|DAY|2021-05-14|||||||||||||||0|2021-05-14 08:59:01:045|||" \
                "|||||149823|M|TDA|N||||||N||||A|||||||N|REG|Y|||||||||1"

    split_strings = in_string.split("|")
    print(len(split_strings))
    print(f"{split_strings[0]}")



if __name__ == "__main__":
    main()

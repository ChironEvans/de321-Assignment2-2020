# code by Liam Beaver
# define the name of the file to read from
filename = input("what is the name of the file")

# open the file for reading
try:
    filehandler = open(filename, "r")
    while True:
        # read a single line
        line = filehandler.readline()
        if not line:
            break
        print(line)

    # close the pointer to that file
    filehandler.close()
except FileNotFoundError:
    print("This file does not exist")

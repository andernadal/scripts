import pandas as pd
import sys
from colorama import Fore, Back, Style


if (len(sys.argv) >= 2):
    FILE = sys.argv[1]
else:
    print(Fore.RED + "No file name , please give the file name, (NO EXTENSION) to convert it!")
    print(Style.RESET_ALL)
    sys.exit(1)

FILE=FILE.strip()
FILE_IN = FILE + ".csv"
FILE_OUT = FILE + ".xlsx"

try:
    read_file = pd.read_csv (FILE_IN)
    read_file.to_excel (FILE_OUT, index = None, header=True)
except:
    print(Fore.LIGHTRED_EX + "ERROR! Check file name or permissions!")
    print(Style.RESET_ALL)
    sys.exit(1)

print(Fore.LIGHTWHITE_EX + FILE_IN + " sucessfuly converted to " + FILE_OUT)
print(Style.RESET_ALL)
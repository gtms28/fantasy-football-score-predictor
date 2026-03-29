
import helper
import pandas as pd
# import helperTwo
# import footballQuarterbackWhatever

command = -1
while command != 0:
    print()
    print("** Position List **")
    print("1. Quarterback")
    print("2. Running Back")
    print("3. Wide Receiver")
    print()
    print("** Other **")
    print("4. Score Calculator")
    print("0. Quit")
    command = int(input("What is your command? "))
    
    if command == 1:
        print("Score Predictor -- Quarterback")
        helper.quarterback()
    elif command == 2:
        print("Score Predictor -- Running Back")
        helper.runningback()
    elif command == 3:
        print("Score Predictor -- Wide Receiver")
        helper.widereceiver()
    elif command == 4:
        print("Score Calculator")
        helper.calculator()
    elif command == 0:
        print("See you next time!")

print("Program complete")

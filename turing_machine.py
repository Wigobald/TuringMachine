import json
import sys
import re
from jff_converter import convert

# Getting file and input string
if len(sys.argv) == 3:
    filename = sys.argv[1]
    input_string = sys.argv[2]
else:
    print("Arguments not valid/found.")
    filename = "ej1.json"
    input_string = "111"

if filename.endswith(".json"):
    data = open(filename, 'r')
    tm = json.load(data)
    data.close()
    jff = False
elif filename.endswith(".jff"):
    tm = convert(filename)
    jff = True
    print("WARNING: Will not check for valid input/output symbols due to .jff limitations."
          " State names may not be accurate")
else:
    print("File not valid.")
    exit()

# Turing machine
state = tm['q0']
position = 0
accepted = True  # Whether the string was accepted or not
print(f"Tape: {input_string}")
while state not in tm['F']:
    if position < 0 or position >= len(input_string):
        value = '#'
    else:
        value = input_string[position]
        if input_string[position] not in tm['Sigma'] and not jff:  # check input in sigma
            print(f"'{value}' is not a valid input symbol.")
            accepted = False
            break

    found = False  # Whether the symbol has a defined transition
    for q in tm['Delta'][state]:
        if value == q:
            found = True
            if tm['Delta'][state][q]['e'] not in tm['Gamma'] and not jff:  # check output in gamma
                print(f"'{value}' is not a valid output symbol.")
                accepted = False
                break

            # Write
            if position < 0:
                input_string = tm['Delta'][state][q]['e'] + input_string
            elif position >= len(input_string):
                input_string = input_string + (tm['Delta'][state][q]['e'])
            else:
                input_string = list(input_string)
                input_string[position] = tm['Delta'][state][q]['e']
                input_string = "".join(input_string)

            # Print the tape
            if value != tm['Delta'][state][q]['e']:
                print(f"Tape: {input_string}")

            # Move
            if tm['Delta'][state][q]['m'] == 'r':
                position += 1
            elif tm['Delta'][state][q]['m'] == 'l':
                position -= 1

            # Transition
            state = tm['Delta'][state][q]['q']

            break

    if not found:
        print(f"Could not find a transition for the symbol '{value}' in the state '{state}'.")
        accepted = False
        break


# Output
if accepted:
    print("String accepted.")
    input_string = input_string.replace("#", " ", -1)
    result = re.search(r"(\s*)(\S*)(\s*)", input_string)  # Remove irrelevant blank spaces
    print(f"Output: '{str(result.group(2))}'")
else:
    print("String rejected.")

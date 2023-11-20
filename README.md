# TuringMachine
A python script that runs a turing machine on the command line.

Accepts JFLAP files (.jff) as well .json files, check the examples.

# Usage

python turing_machine.py tm.json/tm.jff string

Example:

python turing_machine.py example_contains_010.jff 111010111

Output:

Tape: 111010111
String accepted.
Output: '111010111'

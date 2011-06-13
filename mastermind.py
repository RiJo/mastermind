#!/usr/bin/python

from sys import argv, exit, stdout
import random

# Global variables
keypegs = [' ','.','O']
codepegs = ['1','2','3','4','5','6']
code_length = 4
codepeg_count = 6
turn_count = 10

def usage():
    stdout.write("" + argv[0] + " [-t turns] [-n codepegs] [-h]\n")
    stdout.write("   -h, --help                  Printouts this help\n")
    stdout.write("   -c, --codepegs=count        Code peg count (colors) used\n")
    stdout.write("   -t, --turns=count           Number of turns to guess the pattern\n")

def intro():
    stdout.write("--------------------------------------------------------\n")
    stdout.write("  MasterMind, by RiJo\n")
    stdout.write("--------------------------------------------------------\n")
    stdout.write("    Code length: " + str(code_length) + "\n")
    stdout.write("    Turn count: " + str(turn_count) + "\n")
    stdout.write("    Code peg count: " + str(codepeg_count) + "\n")
    stdout.write("    Key pegs:")
    for keypeg in keypegs:
        stdout.write(" '" + keypeg + "'")
    stdout.write("\n")
    stdout.write("    Code pegs:")
    for codepeg in codepegs:
        stdout.write(" '" + codepeg + "'")
    stdout.write("\n")
    stdout.write("--------------------------------------------------------\n")

def start():
    # Handle args
    if "-h" in argv or "--help" in argv:
        usage()
        exit()
    
    code = "".join(random.sample(codepegs, code_length))
    stdout.write("Randomized code: " + code + "\n")
    
    # Start game
    if game(code, 1) == 1:
        stdout.write("\nCongratulations!\n")
    else:
        stdout.write("\nGame over!\n")

def evaluate(code, input):
    # Validity check
    if len(input) != code_length:
        stdout.write("--- Invalid length ---\n")
        return 0
    for char in input:
        if not char in codepegs:
            stdout.write("--- Invalid code peg (" + char + ") detected ---\n")
            return 0
    
    # Code evaluation
    result = []
    unused = range(code_length)
    for i in range(code_length):
        if code[i] == input[i]:
            unused.remove(i)
            result.append(2)
            continue
        for j in unused:
            if code[i] == input[j]:
                unused.remove(j)
                result.append(1)
                i += 1
                continue
    for i in unused:
        result.append(0)
    
    stdout.write("Result: ")
    result.sort()
    for i in result:
        stdout.write(" " + keypegs[i])
    stdout.write("\n")
    return 1

def game(code, turn):
    if turn > turn_count:
        return 0 # Game over
    
    input_pattern = raw_input("#" + str(turn) + " > ")
    if not evaluate(code, input_pattern):
        return game(code, turn) # Restart turn
    
    if input_pattern == code:
        return 1 # Pattern matched
    else:
        return game(code, turn + 1)

intro()
start()

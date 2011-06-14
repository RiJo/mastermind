#!/usr/bin/python

from sys import argv, exit, stdout
import random

# Global variables
keypegs = [' ','.','O']
codepegs = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
code_length = 4
codepeg_count = 6
turn_count = 10
exit_commands = ["exit","e","quit","q"]

def usage():
    stdout.write("" + argv[0] + " [-h] [-n codepegs] [-t turns]\n")
    stdout.write("   -h, --help                  printouts this help\n")
    stdout.write("   -c, --codepegs=count        code peg count (colors) used, default " + str(codepeg_count) + "\n")
    stdout.write("   -t, --turns=count           number of turns to guess the pattern, default " + str(turn_count) + "\n")
    exit()

def intro():
    stdout.write("--------------------------------------------------\n")
    stdout.write("  mastermind                             by RiJo  \n")
    stdout.write("--------------------------------------------------\n")
    stdout.write("  turns: " + str(turn_count) + "\n")
    stdout.write("  code length: " + str(code_length) + "\n")
    stdout.write("  code pegs: " + ", ".join(codepegs[0:codepeg_count]) + "\n")
    stdout.write("--------------------------------------------------\n")

def start():
    # Handle args
    if "-h" in argv or "--help" in argv:
        usage()
    else:
        intro()
    
    code = "".join(random.sample(codepegs[0:codepeg_count], code_length))
    #stdout.write("Randomized code: " + code + "\n")
    
    # Start game
    if game(code, 1) == 1:
        stdout.write("  congratulations!\n")
    else:
        stdout.write("  game over!\n")
    stdout.write("--------------------------------------------------\n")

def evaluate(code, input):
    # Validity check
    if len(input) != code_length:
        stdout.write("--- invalid length ---\n")
        return 0
    for char in input:
        if not char in codepegs[0:codepeg_count]:
            stdout.write("--- invalid code peg ---\n")
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
                break
    for i in unused:
        result.append(0)
    
    # Print out result
    stdout.write("                          ")
    for i in input:
        stdout.write(" " + i)
    stdout.write("      ")
    result.sort()
    for i in result:
        stdout.write(" " + keypegs[i])
    stdout.write("\n")
    return 1

def game(code, turn):
    if turn > turn_count:
        return 0 # Game over
    
    input_pattern = raw_input(" #" + str(turn).zfill(2) + "  ")
    if input_pattern in exit_commands:
        return 0 # Exit forced
    if not evaluate(code, input_pattern):
        return game(code, turn) # Restart turn
    
    if input_pattern == code:
        return 1 # Pattern matched
    else:
        return game(code, turn + 1)

start()
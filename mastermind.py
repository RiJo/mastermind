#!/usr/bin/python

from signal import signal, SIGINT
from sys import argv, exit, stdin, stdout
from getopt import getopt
from random import randrange

# Add signal handler for ctrl-c
def signal_handler(signal, frame):
    stdout.write('\nAborted, ctrl-c pressed\n')
    exit(0)
signal(SIGINT, signal_handler)

# Global variables
keypegs = [' ','.','O']
codepegs = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
code_length = 4
codepeg_count = 6
turn_count = 10
exit_commands = ["exit","e","quit","q"]

def usage():
    stdout.write("" + argv[0] + " [-h] [-c codepegs] [-l length] [-t turns]\n")
    stdout.write("   -h, --help                  print out this help\n")
    stdout.write("   -c, --codepegs=count        code peg count (colors) used, default " + str(codepeg_count) + "\n")
    stdout.write("   -l, --length=length         length of the code, default " + str(code_length) + "\n")
    stdout.write("   -t, --turns=count           number of turns to guess the pattern, default " + str(turn_count) + "\n")
    exit()

def header():
    stdout.write("--------------------------------------------------\n")
    stdout.write("  mastermind v0.2                        by RiJo  \n")
    stdout.write("--------------------------------------------------\n")
    stdout.write("  turns: " + str(turn_count) + "\n")
    stdout.write("  code length: " + str(code_length) + "\n")
    stdout.write("  code pegs: " + ", ".join(codepegs[0:codepeg_count]) + "\n")
    stdout.write("--------------------------------------------------\n")

def footer():
    stdout.write("--------------------------------------------------\n")

def start():
    global codepeg_count, code_length, turn_count

    # Handle args
    opts, args = getopt(argv[1:], "hc:l:t:", ["help","codepegs=","length=","turns="])
    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            usage()
        elif "-c" in opt[0] or "--codepegs=" in opt[0]:
            codepeg_count = int(opt[1])
        elif "-l" in opt[0] or "--length=" in opt[0]:
            code_length = int(opt[1])
        elif "-t" in opt[0] or "--turns=" in opt[0]:
            turn_count = int(opt[1])

    code = ''.join([codepegs[randrange(0, codepeg_count)] for x in range(code_length)])
    stdout.write("Randomized code: " + code + "\n")

    # Start game
    header()
    if game(code, 1) == 1:
        stdout.write("\n  congratulations!\n")
    else:
        stdout.write("\n  game over!                     solution: " + code + "     \n")
    footer()

def game(code, turn):
    if turn > turn_count:
        return 0 # Game over
    
    stdout.write(" #" + str(turn).zfill(2) + "  ")
    stdout.flush()
    input_pattern = stdin.readline().strip()
    if input_pattern in exit_commands:
        return 0 # Exit forced
    
    if not evaluate(code, input_pattern):
        return game(code, turn) # Restart turn
    
    if input_pattern == code:
        return 1 # Pattern matched
    else:
        return game(code, turn + 1) # Next turn

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
    unused = [x for x in range(code_length)]
    for i in range(code_length):
        if code[i] == input[i]:
            unused.remove(i)
            result.append(2)
            continue
        for j in unused:
            if code[i] == input[j] and code[j] != input[j]:
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

start()
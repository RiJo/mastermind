#!/usr/bin/python

from sys import argv, exit
import random

# Global variables
keypegs = [' ','.','O']
codepegs = ['1','2','3','4','5','6']
code_length = 4
codepeg_count = 6
turn_count = 10

def usage():
    print argv[0],"[-t turns] [-n codepegs] [-h]"
    print "   -h, --help                  Printouts this help"
    print "   -c, --codepegs=count        Code peg count (colors) used"
    print "   -t, --turns=count           Number of turns to guess the pattern"

def intro():
    print "--------------------------------------------------------"
    print "  MasterMind, by RiJo"
    print "--------------------------------------------------------"
    print "  Code length:", code_length
    print "  Turn count:", turn_count
    print "  Code peg count:", codepeg_count
    print ""
    print "  Key pegs: ",
    for keypeg in keypegs:
        print " ",keypeg,
    print ""
    print "  Code pegs:",
    for codepeg in codepegs:
        print " ",codepeg,
    print ""
    print "--------------------------------------------------------"

def start():
    # Handle args
    if "-h" in argv or "--help" in argv:
        usage()
        exit()
    
    code = "".join(random.sample(codepegs, code_length))
    print "Randomized code:",code
    
    # Start game
    if game(code, 1) == 1:
        print "Congratulations!"
    else:
        print "Game over!"

def evaluate(code, input):
    # Validity check
    if len(input) != code_length:
        print "--- Invalid length ---"
        return 0
    for char in input:
        if not char in codepegs:
            print "--- Invalid code peg (",char,") detected ---"
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
    
    print "Result: ",
    result.sort()
    for i in result:
        print " ",keypegs[i],
    print ""
    return 1

def game(code, turn):
    if turn > turn_count:
        return 0 # Game over
    
    print "Turn #", turn
    input_pattern = raw_input("> ")
    if not evaluate(code, input_pattern):
        return  game(turn) # Restart turn
    
    # Print key pegs (result)
    if input_pattern == code:
        return 1 # Pattern matched
    else:
        return game(code, turn + 1)

intro()
start()

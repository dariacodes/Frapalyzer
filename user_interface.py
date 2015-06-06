# coding=utf-8
import os, sys

def exit():
    print "Bye..."
    sys.exit()
    pass

actions = [
    ("Create an apocope dictionary from parsed sources", lambda: os.system("python ./create_dict_apo_auto.py")),
    ("Create an apocope dictionary augmented with stats", lambda: os.system("python ./create_dict_apo_aug.py")),
    ("Create a blacklist of cut parts", lambda: os.system("python ./create_blacklist_cut.py")),
    ("Create a frequency dictionary from le Point articles", lambda: os.system("python ./create_datasets.py")),
    ("Create a set of comparisons of algorithm improvements based on 'data/list_words'", lambda: os.system("python ./create_imp_comp.py")),
    ("Exit", exit)
]

def get_choice():
    print "Hi, here's what we can do:"
    print "\r\n".join(["    %s. %s" % (i+1, actions[i][0]) for i in range(len(actions))])
    print
    print "What would you like to do?"
    while True:
        try:
            choice = int(raw_input("> "))
            return choice
        except:
            pass

while True:
    choice = get_choice()
    print
    try:
        actions[choice-1][1]()
    except SystemExit:
        break
    except:
        print "Could not complete the command"
    print
    raw_input("Press Enter to continue...")
    print
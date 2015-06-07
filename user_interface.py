# coding=utf-8
import os, sys
import apocopes_in_french as aif
import create_datasets as credat

def try_alg():
    def try_is_apocope():
        while True:
            apo = ""
            print "Enter a potential apocope:"
            apo = raw_input("> ")
            if not apo:
                break
            fulls = aif.find_fulls(apo)
            if fulls:
                print "Potential full forms:"
                print ', '.join(fulls)
            else:
                print "'" + apo + "' is not an apocope"
            print

    def try_is_apocope_of():
        while True:
            apo, full = "", ""
            print "Enter a potential apocope:"
            apo = raw_input("> ")
            if not apo:
                break
            print "Enter a potential full form:"
            full = raw_input("> ")
            if not full:
                break
            if aif.is_apocope_of(apo, full):
                print "'" + apo + "' is an apocope of '" + full + "'"
            else:
                print "'" + apo + "' is not an apocope of '" + full + "'"
            print

    actions_try = [
        ("Check if the inserted word is an apocope", try_is_apocope),
        ("Check if the inserted word is an apocope of the inserted full form", try_is_apocope_of),
        ("Return to the main menu", main_menu),
    ]
    while True:
        exec_action(actions_try)

def create_own_datasets():
    print "Enter a path to your data:"
    p = raw_input("> ")
    credat.proc(p)


def exec_action(acts):
    def get_choice(acts):
        print "Here's what we can do:"
        print "\r\n".join(["    %s. %s" % (i+1, acts[i][0]) for i in range(len(acts))])
        print
        print "What would you like to do?"
        while True:
            try:
                choice = int(raw_input("> "))
                return choice
            except:
                pass

    choice = get_choice(acts)
    print
    try:
        acts[choice-1][1]()
    except SystemExit:
        raise
    except:
        print "Could not complete the command"


def main_menu():
    def exit():
        print "Bye..."
        sys.exit()

    actions_main = [
        ("Create an apocope dictionary from parsed sources", lambda: os.system("python ./create_dict_apo_auto.py")),
        ("Create an apocope dictionary augmented with stats", lambda: os.system("python ./create_dict_apo_aug.py")),
        ("Create a blacklist of cut parts", lambda: os.system("python ./create_blacklist_cut.py")),
        ("Create a frequency dictionary from Le Point articles", lambda: os.system("python ./create_datasets.py")),
        ("Create a frequency dictionary from your own file", create_own_datasets),
        ("Create a set of comparisons of algorithm improvements based on 'data/list_words'", lambda: os.system("python ./create_imp_comp.py")),
        ("Try the algorithm out", try_alg),
        ("Exit", exit)
    ]
    while True:
        exec_action(actions_main)
        raw_input("Press Enter to continue...")
        print

try:
    print "Hi!"
    main_menu()
except SystemExit:
    pass

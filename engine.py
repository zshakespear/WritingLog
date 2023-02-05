# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 10:10:43 2023

This program is meant to use the commnad line to help log the number of words written

The command line should take one argument for the user, one argument for -d (drafting), -p (prepping), or -e (editing) and then an integer. In the case of d, the integer is the number of words. In the case of e or p, the integer is the number of minutes spent editing.

-r means retrieve and then the integer is replaced by the date

-i means initialize a new user, then -e and two integers. The first integer is a number of minutes, the second is the number of words. Then comes -p and two integers as above.

-n means delete. The program will display the log and allow the user to select the index of the entry to be deleted. 

-v means visualize. Instead of an integer, a new flag will follow
-s means standard: a graphical visualization of words over time will be saved to the desktop
-pw means pie words: a graphical visualization of words editing versus words drafting
-pt means pie time: a graphical visualization of time editing versus time drafting

-t means tag and the integer is then replaced with a name for the project. 

@author: zacos
"""
#TODO: allow tagging words with certain projects
#TODO: allow graphical visualization of words over time
#TODO: allow graphical visualization of words editing versus words drafting
#TODO: allow graphical visualization of time editing versus time drafting

import sys
import os
import pandas as pd
import user as u

root = 'c://users/zacos/Desktop/pyRepos/WritingLog/'
help_message = 'Type -h for help.'

def comm_errCheck():
    if sys.argv[2] == '-r':
        if len(sys.argv) != 4:
            print('Wrong number of arguments', help_message)
            sys.exit() 
        else:
            arg_check('-r')
    elif sys.argv[2] == '-d' or sys.argv[2] == '-e' or sys.argv[2] == '-p':
        if len(sys.argv) in (4,5,6) == False:
            print('Wrong number of arguments.',help_message)
            sys.exit()
        elif sys.argv[2] == '-d':
            arg_check('-d')
        elif sys.argv[2] == '-e' or sys.argv[2] == '-p':
            arg_check('-e')
    elif sys.argv[2] == '-n':
        if len(sys.argv) != 3:
            print('Wrong number of arguments',help_message)
            sys.exit()
    else:
        print('Command not recognized.', help_message)
        
def arg_check(mode):
    if mode == '-d':
        try: int(sys.argv[3])
        except:
            print('Non-int value at sys.argv[3].',help_message)
            sys.exit()
    elif mode == '-e':
        try: int(sys.argv[3])
        except:
            try: float(sys.argv[3])
            except:
                print('Non-numerical value at sys.argv[3].',help_message)
                sys.exit()
    elif mode == '-r':
        try: str(sys.argv[3])
        except:
            print('Non-string value at sys.argv[3].', help_message)
            sys.exit()
        if len(sys.argv[3]) != 10:
            print('Date is not the right length.', help_message)
            sys.exit()
    else:
        print('Mode in arg_check not recognized')

def unpack_args():
    args = []
    for i in sys.argv:
        args.append(i)
    return args

def get_users():
    user_list = [x[0] for x in os.walk(root)]
    users = []
    for el in user_list:
        new_el = el[len(root):]
        users.append(new_el)
        del new_el
    return users
        

def check_user(user_q):
    users = get_users()
    if user_q in users:
        print('Found User')
        return True
    else:
        print('Did not find user')
        return False

def float_loop(message):
    while True:
        out = input(message)
        try: int(out)
        except:
            try: float(out)
            except:
                print('Non numerical value. Please try again.')
            else:
                return float(out)
        else:
            return int(out)

def int_loop(message):
    while True:
        out = input(message)
        try: int(out)
        except:
            print('Non numerical value. Please try again.')
        else:
            return int(out)

def help_flag():
    if sys.argv[1] == '-h':
        with open(root+'helpfile.txt') as f:
            for x in f:
                print(x)
        sys.exit()
    
def user_init(name):
    print("User not found. Initializing new profile:")
    print('Initizializing conversion minutes to words:')
    minutes0 = float_loop('Enter number of minutes')
    words0 = int_loop('Enter number of words')
    log_add = root+name+'/log.csv'
    new_log = pd.DataFrame(columns = ['date','words','mode'])
    new_log.to_csv(log_add,index=False)
    
    init = {
        'username':name,
        'conv':words0/minutes0,
        'log_add':log_add
        }
    u.user(init).to_json(root+name)
    return u.user(init)
    
def main():
    help_flag()
    args = unpack_args()
    username = args[1]
    try: user_obj = u.user(root+username+'/user.json')
    except: user_obj = user_init(username)
    flag = args[2]
    if flag in ('-d','-e','-p'):
        num2add = args[3]
        try: date = args[4]
        except: date = None
        finally: user_obj.add_words(num2add,flag[1],date)
    elif flag=='-n':
        print(user_obj.log)
        drop = int_loop("Enter the index of the entry you wish to delete\n")
        user_obj.drop_entry(drop)
    elif flag == '-r':
        rdate = args[3]
        rint = user_obj.retreive(rdate)
        print('Total words on',rdate,"is:",rint)

main()
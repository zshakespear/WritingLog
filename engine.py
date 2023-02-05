# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 10:10:43 2023

This program is meant to use the commnad line to help log the number of words written

The command line should take one argument for the user, one argument for -d (drafting) or -e (editing) and then an integer. In the case of d, the integer is the number of words. In the case of e, the integer is the number of minutes spent editing.

-r means retrieve and then the integer is replaced by the date

-i means initialize a new user, then -e and two integers. The first integer is a number of minutes, the second is the number of words. Then comes -p and two integers as above.

-n means delete. The program will display the log and allow the user to select the index of the entry to be deleted. 

-v means visualize. Instead of an integer, a new flag will follow
-s means standard: a graphical visualization of words over time will be saved to the desktop
-pw means pie words: a graphical visualization of words editing versus words drafting
-pt means pie time: a graphical visualization of time editing versus time drafting

-t means tag and the integer is then replaced with a name for the project. 

-p means prep and there should be a separate conversion for that (lines 2 & 3)

@author: zacos
"""
#TODO: add -p
#TODO: allow initialization of new users
#TODO: allow tagging words with certain projects
#TODO: allow graphical visualization of words over time
#TODO: allow graphical visualization of words editing versus words drafting
#TODO: allow graphical visualization of time editing versus time drafting

import sys
import os
import pandas as pd
from datetime import date
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

def check_log(user_q):
    try: log = pd.read_csv(root+user_q+'/log.csv')
    except:
        print('Initializing new log')
        new_log = pd.DataFrame(columns = ['date','words','mode'])
        new_log.to_csv(root+user_q+'/log.csv',index=False)

def check_conv(user_q):
    try: f = open(root+user_q+'/conv.txt')
    except:
        print('Conversion file not found. Initializing...')
        conv_init(user_q)
    else:
        length_test = []
        for x in f:
            length_test.append(x)
        if len(length_test) != 4:
            print('Conversion file is incomplete. Rewriting...')
            conv_init(user_q)
            
def conv_init(user_q):
    print('Editing conversion minutes to words:')
    minutes0 = float_loop('minutes')
    words0 = int_loop('words')
    print('Prep conversion minutes to words:')
    minutes1 = float_loop('minutes')
    words1 = int_loop('words')
    f = open(root+user_q+'/conv.txt','w')
    f.write(minutes0+'\n')
    f.write(words0+'\n')
    f.write(minutes1+'\n')
    f.write(words1+'\n')
    f.close()

def float_loop(message):
    while True:
        out = input('Enter number of '+message)
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
        out = input('Enter number of '+message)
        try: int(out)
        except:
            print('Non numerical value. Please try again.')
        else:
            return int(out)

def get_econv(user_q):
    with open(root+user_q+'/conv.txt') as f:
        minutes = f.readline()
        if int(minutes) != float(minutes):
            minutes = float(minutes)
        else:
            minutes = int(minutes)
        words = f.readline()
        if int(words) != float(words):
            words = float(words)
        else:
            words = int(words)
    conv = words/minutes
    return conv

def get_pconv(user_q):
    with open(root+user_q+'/conv.txt') as f:
        f.readline()
        f.readline()
        minutes = f.readline()
        if int(minutes) != float(minutes):
            minutes = float(minutes)
        else:
            minutes = int(minutes)
        words = f.readline()
        if int(words) != float(words):
            words = float(words)
        else:
            words = int(words)
    conv = words/minutes
    return conv

def add_entry(user_q,mode, num, indate=None):
    if mode == '-d' and indate==None:
        new_entry = pd.DataFrame(
            {'date': date.today(),
             'words':int(num),
             'mode':'d'},
            index=[0])
    if mode == '-e' and indate == None:
        new_entry = pd.DataFrame(
            {'date':date.today(),
             'words':int(num)*get_econv(user_q),
             'mode':'e'},
             index=[0])
    if mode == '-d' and indate!=None:
        new_entry = pd.DataFrame(
            {'date': indate,
             'words':int(num),
             'mode':'d'},
            index=[0])
    if mode == '-e' and indate!=None:
        new_entry = pd.DataFrame(
            {'date': indate,
             'words':int(num),
             'mode':'d'},
            index=[0])
    log = pd.read_csv(root+user_q+'/log.csv')
    log = pd.concat([log, new_entry],ignore_index=True)
    log.to_csv(root+user_q+'/log.csv',index=False)
    
def retrieve(user_q, date):
    log = pd.read_csv(root+user_q+'/log.csv')
    total = log[log['date']==date]['words'].sum()
    print('Total words on',date,'is:',int(total))

def help_flag():
    if sys.argv[1] == '-h':
        with open(root+'helpfile.txt') as f:
            for x in f:
                print(x)
        sys.exit()

def del_entry(userq):
    log = pd.read_csv(root+userq+'/log.csv')
    print(log)
    to_del = int_loop('the index of the entry you wish to delete\n')
    log.drop(labels=to_del,axis=0,inplace=True)
    log.to_csv(root+userq+'/log.csv',index=False)
    

def main():
    help_flag()
    comm_errCheck()
    if len(sys.argv) == 4:
        args = unpack_args()
        user_q = args[1]
        mode = args[2]
        num2add = args[3]
        date2add = None
    elif len(sys.argv) == 3:
        args = unpack_args()
        user_q = args[1]
        mode = args[2]
        date2add=None
    elif len(sys.argv) == 5:
        args = unpack_args()
        user_q=args[1]
        mode = args[2]
        num2add = args[3]
        date2add = args[4]
    else:
        print("Wrong number of arguments",help_message)
        sys.exit()
    check_log(user_q)
    if mode == '-d' or mode == '-e':
        check_conv(user_q)
        add_entry(user_q, mode, num2add, date2add)
    if mode == '-r':
        retrieve(user_q, num2add)
    if mode == '-n':
        del_entry(user_q)

main()
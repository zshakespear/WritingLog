# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 17:00:36 2023

This user class is meant to work with the engine in order to make engine a little less unwieldy

@author: zacos
"""

import json
import pandas as pd
from multipledispatch import dispatch as dp
import date

class user(object):
    root = 'c://users/zacos/Desktop/pyRepos/WritingLog/'
    
    @dp(str)
    def __init__(self, file):
        with open(file,'r') as f:
            obj = json.load(f)
        self.username = obj['username']
        self.econv = obj['econv']
        self.pconv = obj['pconv']
        url = obj['log_add']
        self.log = pd.read_csv(url)
    
    @dp(dict)
    def __init__(self, indict):
        self.username = indict['username']
        self.econv = indict['econv']
        self.pconv = indict['pconv']
        url = indict['log_add']
        self.log = pd.read_csv(url)
        
    def save_log(self, path):
        self.log.to_csv(path,index=False)
        
    def to_json(self, path):
        self.save_log(path+'/log.csv')
        outdict = {
            'username':self.username,
            'econv':self.econv,
            'pconv':self.pconv,
            'log_add':self.root+self.username+'/log.csv',
            }
        with open(path+'/user.json','w') as f:
            json.dump(outdict,f)
    
    def add_words(self, numwords, flag, indate = None):
        if flag == 'e':
            numwords *= self.econv
        elif flag == 'p':
            numwords *= self.pconv
        if indate != None:
            new_entry = pd.DataFrame(
                {'date': indate,
                 'words':numwords,
                 'mode':flag},
                index=[0])
        else:
                new_entry = pd.DataFrame(
            {'date': date.today(),
             'words':numwords,
             'mode':'d'},
            index=[0])
        self.log = pd.concat([self.log, new_entry],ignore_index=True)
    
    def drop_entry(self, ind):
        self.log.drop(ind,inplace=True)
    
    def retreive(self, indate):
        total = self.log[self.log['date']==indate]['words'].sum()
        return int(total)
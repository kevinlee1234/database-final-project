import numpy as np
import re
import csv
from itertools import groupby
from operator import itemgetter

class Table:
    def __init__(self, table = [], index = None):
        self.table = table
        self.index = index

    @classmethod
    def inputfromfile(cls,file):
        ''' This function imports the csv data file and transform it to a table.
            Input: A opened csv file
            Output: A table with a list of dictionary
        '''
        filename = str(file) + '.csv'
        df = []
        with open(filename,encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            columns = next(reader)[0].split('|')
            data = [r[0].strip().split('|') for r in reader]
        
        for i in range(len(data)): 
            res = {}
            for k in range(len(data[0])):
                try:
                    res[columns[k]] = float(data[i][k])
                except ValueError:
                    res[columns[k]] = data[i][k]
            df.append(res)
        
        return df

        @classmethod
        def select(cls, table, conditions,query):
            ''' This function selects rows according to conditions in the table
                Inputs: dataframe, a list of conditions and the original query
                Output: Required data dictionary 
            '''
            data_under_condition = []
            if 'and' in query:
                string = ', '.join(conditions)
                code = to_code(string)
                for df in table:
                    if eval(code):
                        data_under_condition.append(df)
            elif 'or' in query:
                string = '; '.join(conditions)
                code = to_code(string)
                for df in table:
                    if eval(code):
                        data_under_condition.append(df)
            else:
                code = to_code(string)
                for df in table:
                    if eval(code):
                        data_under_condition.append(df)
                        
            return data_under_condition

def to_code(string):
    ''' This function transfer conditions to code that can be evaluated by the eval function
        Input: All the conditions in one string
        Output: Code to be evaluated 
    '''
    cols = re.findall('[a-zA-Z]+',string)
    for i in cols:
        string = re.sub(i, "df['%s']" % i, string)
    
    string = string.replace(',', ' and ')
    string = string.replace(',', ' or ')
    if '=' in string and '>=' not in string and '<=' not in string:
        string = string.replace('=', '==')
    
    return string

def projection(Df,conditions):
    
    ''' This function select columns from data table
        Inputs: dataframe and a list of columns
        Output: table with these columns 
    '''
    data_under_conditions = []
    for i in range(len(Df)):
        data_under_conditions.append(dict((k, Df[i][k]) for k in conditions))
        
    return data_under_conditions

def avg(Df,condition):
    
    ''' This function calculates the average of a given column
        Inputs: dataframe and a list of column
        Output: average of that column 
    '''
    
    col = condition[0]
    sum_ = 0
    for i in range(len(Df)):
        sum_ = sum_ + Df[i][col]
        
    return sum_ / len(Df)

def sumgroup(Df,conditions):
    
    ''' This function calculates the sum of a given column for different groups 
        Inputs: dataframe and a list of column and groups 
        Output: sum of a specific column for different groups 
    '''
    
    col = conditions[0]
    groups = tuple(conditions[1:])
    group_func = itemgetter(*groups)
    sorted_Df = sorted(Df, key = group_func)
    
    grouped_data =  [(key,list(group)) for key, group in groupby(sorted_Df, group_func)]
    keys = []
    values = []
    for i in range(len(grouped_data)):
        keys.append(grouped_data[i][0])
        values.append(grouped_data[i][1])
    
    sum_group = []
    for i in values:
        sum_ = 0
        for j in i:
            sum_ += j[col]
        sum_group.append(sum_)
        
    data_under_conditions = {keys[i]: sum_group[i] for i in range(len(sum_group))} 
    
    return data_under_conditions

def avggroup(Df,conditions):
    
    ''' This function calculates the average of a given column for different groups 
        Inputs: dataframe and a list of column and groups 
        Output: average of a specific column for different groups 
    '''
    
    col = conditions[0]
    groups = tuple(conditions[1:])
    group_func = itemgetter(*groups)
    sorted_Df = sorted(Df, key = group_func)
    
    grouped_data =  [(key,list(group)) for key, group in groupby(sorted_Df, group_func)]
    keys = []
    values = []
    for i in range(len(grouped_data)):
        keys.append(grouped_data[i][0])
        values.append(grouped_data[i][1])
    
    sum_group = []
    for i in values:
        sum_ = 0
        for j in i:
            sum_ += j[col]
        sum_group.append(sum_ / len(i))
        
    data_under_conditions = {keys[i]: sum_group[i] for i in range(len(sum_group))} 
    
    return data_under_conditions


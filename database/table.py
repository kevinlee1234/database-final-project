import numpy as np
import re
import csv
from itertools import groupby
from operator import itemgetter
from database.parser import input_parser, construct_condition



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
        f.close()
        return cls(df)

    @classmethod
    def select(cls, table, conditions):
        ''' This function selects rows according to conditions in the table
            Inputs: table    : Table
                    condtion : str
            Output: Table
        '''
        data_under_condition = []
        row_condition = construct_condition(conditions,table='row')
        for row in table.table:
            if eval(row_condition):
                data_under_condition.append(row)
        return cls(data_under_condition)

    @classmethod
    def join(cls, A, B, A_name, B_name, condition):
        '''This function join two table according to the condition
           Inputs: A         : Table
                   B         : Table
                   A_name    : str, name of table A
                   B_name    : str, name of table B
                   condtion  : str
           Output: Table
        '''
        table = {A_name:'A_row', B_name:'B_row'}
        row_condition = construct_condition(condition, tableName = table)
        output = []
        for A_row in A.table:
            for B_row in B.table:
                if eval(row_condition):
                    new_row = {}
                    for key in A_row:
                        column = '{}_{}'.format(A_name,key)
                        new_row[column] = A_row[key]
                    for key in B_row:
                        column = '{}_{}'.format(B_name,key)
                        new_row[column] = B_row[key]
                    output.append(new_row)
        return cls(output)
                
    @classmethod
    def projection(cls, table, table_name,parameter):
        ''' This function select columns from data table
            Inputs: table      : Table
                    table_name : str, the name of table
                    paramter   : list, contains the columns name we need to project
            Output: table with these columns 
        '''
        output = []
        for row in table.table:
            new_row = {}
            for column in parameter:
                new_column = '{}_{}'.format(table_name, column)
                new_row[new_column] = row[column]
            output.append(new_row)
        return cls(output)
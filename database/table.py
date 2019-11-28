import re
import csv
from itertools import groupby
from operator import itemgetter
from database.parser import input_parser, construct_condition

class Table:
    def __init__(self, table = [],index = None):
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
        row_condition, columns = construct_condition(condition, tableName = table)
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
    def projection(cls, table, table_name, parameter):
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
                new_row[column] = row[column]
            output.append(new_row)
        return cls(output)

    @classmethod
    def avg(cls, table, column):
        ''' This function calculates the average of a given column
            Inputs: table  : table
                    column : str, we compute the average of this column
            Output: table with single column and single row, the column name will be avg(column)
        '''
        sum = 0
        for row in table.table:
            sum = sum + row[column]
        output_row = {}
        output_row['avg({})'.format(column)] = sum/len(table.table)
        return cls([output_row])

    @classmethod
    def sumgroup(cls,table,conditions):
        ''' This function calculates the sum of a given column for different groups
            Inputs: table      : Table
                    conditions   : list, contains the columns name we need to calculate sum and 
                    the columns we need to group
                    Output: table with sum of a given column for different groups
        '''
        col = conditions[0]
        groups = tuple(conditions[1:])
        group_func = itemgetter(*groups)
        sorted_table = sorted(table.table, key = group_func)

        grouped_data =  [(key,list(group)) for key, group in groupby(sorted_table, group_func)]
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

        data_under_conditions = []
        for i in range(len(sum_group)):
            data_under_conditions.append({keys[i]: sum_group[i]})

        return cls(data_under_conditions)

    @classmethod
    def avggroup(cls,table,conditions):
        ''' This function calculates the average of a given column for different groups
            Inputs: table      : Table
                    table_name : str, the name of table
                    conditions   : list, contains the columns name we need to calculate average and 
                    the columns we need to group
            Output: table with average of a given column for different groups
        '''
        col = conditions[0]
        groups = tuple(conditions[1:])
        group_func = itemgetter(*groups)
        sorted_table = sorted(table.table, key = group_func)

        grouped_data =  [(key,list(group)) for key, group in groupby(sorted_table, group_func)]
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

        data_under_conditions = []
        for i in range(len(sum_group)):
            data_under_conditions.append({keys[i]: sum_group[i]})
            
        return cls(data_under_conditions)

    @classmethod
    def movavg(cls,table,conditions):
        ''' This function calculates the moving average of a given column
            Inputs: table      : Table
                    conditions   : list, contains the table name on which we will operate, the 
                    columns on which we will calculate moving average and the moving step
            Output: table with moving average of a given column
        '''
        col = conditions[1]
        step = int(conditions[2])
        Df = table.table
        moving_avg = []
        for i in range(1,(len(Df)+1)):
            if i <= step:
                sum1 = 0
                data = Df[0:i]
                for j in range(i):
                    sum1 = sum1 + data[j][col]
                moving_avg.append(sum1 / i)
            else:
                sum2 = 0
                data = Df[i-step: i]
                for j in range(step):
                    sum2 = sum2 + data[j][col]
                moving_avg.append(sum2 / step)

        return cls(moving_avg)

    @classmethod
    def movsum(cls,table,conditions):
        ''' This function calculates the moving sum of a given column
            Inputs: table      : Table
                    conditions  : list, contains the table name on which we will operate, the 
                    columns on which we will calculate moving sum and the moving step
            Output: table with moving sum of a given column
        '''
        col = conditions[1]
        step = int(conditions[2])
        Df = table.table
        moving_sum = []
        for i in range(1,(len(Df)+1)):
            if i <= step:
                sum1 = 0
                data = Df[0:i]
                for j in range(i):
                    sum1 = sum1 + data[j][col]
                moving_sum.append(sum1)
            else:
                sum2 = 0
                data = Df[i-step: i]
                for j in range(step):
                    sum2 = sum2 + data[j][col]
                moving_sum.append(sum2)

        return cls(moving_sum)

    @classmethod
    def sort(cls, table, columns):
        '''This function sort the table based on given columns
           Inputs: table   : Table
                   columns : list, The key columns that used to be sorted, can be one or more.
           output: none
        '''
        table.table = sorted(table.table,key = lambda k: [k[column] for column in columns])
        return 

    @classmethod
    def concat(cls, table_A, table_B):
        '''This function concate two tables to one big table
           Inputs: table_A  : Table, this one will be the first part of the new table
                   table_B  : Table, it has the same schema as A
           output: A new table with a contated table from A and B
        '''
        output = table_A.table + table_B.table
        return cls(output)
                   

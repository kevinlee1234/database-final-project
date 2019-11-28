import re

def input_parser(input):
    input = input.replace(" ","") #remove space
    input = input.split('//')[0] #remove comment
    matched = re.findall("(.+):=([^()]+)\((.+)\)",input)
    if matched:
        output_table = matched[0][0]
        function_name = matched[0][1]
        parameter = matched[0][2].split(',')
        return output_table, function_name, parameter
    else:
        raise Exception('Fail to parse. An input should be "R := operation(parameter1, parameter2, ...) but get {}"'.format(input))

def construct_condition(condition, tableName = None, table = None):
    res = condition
    res = re.sub('[^<>!=]=','==',res)
    res = re.sub('={3}', '==', res)
    if tableName:
        columns = re.findall("[a-zA-Z0-9]+[.][a-zA-Z0-9]*", condition)
        for column in columns:
            table, col = column.split('.')
            new_column = tableName[table] + '["{}"]'.format(col)
            res = res.replace(column, new_column)
    elif table:
        columns = re.findall("[a-zA-Z]+[a-zA-Z0-9]*", condition)
        for column in columns:
            if column == "and" or column == "or":
                continue
            new_column = table+'["{}"]'.format(column)
            res = res.replace(column, new_column)
    else:
        raise Exception('Missing input: need tableName for `join` or `table` for `search`')
    return res

def parser(query):
    ''' This function is used to parser the query for the select function
        Input: A query in string format
        Outputs: Table name, function name, table on which we operate and conditions
    '''
    query = query.split('//')[0]
    split = query.split(':=')
    
    ### get the name of generated table
    generate_table_name = split[0].strip()
    
    ### get the name of the table on which we will operate
    q1 = split[1].strip()
    fun_name = q1.split('(')[0]
    operation_table_name = q1.split('(')[1].split(',')[0]
    
    ### get conditions that we will use to operate the table
    conditions = []
    if len(q1.split('(')) == 2:
        for i in range(1,len(q1.split('(')[1].split(','))):
            conditions.append(q1.split('(')[1].split(',')[i].split(')')[0].strip())
    
    if len(q1.split('(')) > 2:
        for i in range(2,len(q1.split('('))):
            conditions.append(q1.split('(')[i].split(')')[0])
            
    return generate_table_name, fun_name, operation_table_name, conditions


if __name__ == '__main__':
    pass
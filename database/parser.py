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



if __name__ == '__main__':
    pass

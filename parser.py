import re
import unittest

def input_parser(input):
    input = input.replace(" ","")
    input = input.split('//')[0] #remove comment
    matched = re.findall("(.+):=([^()]+)\((.+)\)",input)
    if matched:
        output_table = matched[0][0]
        function_name = matched[0][1]
        parameter = matched[0][2].split(',')
        return output_table, function_name, parameter
    else:
        raise Exception('Fail to parse. An input should be "R := operation(parameter1, parameter2, ...) but get {}"'.format(input))

def condition_parser(condition):
    condition_list = []
    condition = condition.replace(" ", "")
    matched = re.findall("\((.+)\)(and|or)\((.+)\)",condition)
    single_condition = re.compile("([^><=!]+)([><=]|[><!][=])([^><=!]+)")
    if(matched):
        condition_list.append(single_condition.findall(matched[0][0])[0])
        condition_list.append(single_condition.findall(matched[0][2])[0])
        return condition_list, matched[0][1]
    else:
        return single_condition.findall(condition)[0],''
        
class TestParser(unittest.TestCase):
    def test_input_parser(self):
        output_table, function_name, parameter = input_parser("R := inputfromfile(sales1) ")
        self.assertEqual('R', output_table)
        self.assertEqual('inputfromfile', function_name)
        self.assertEqual(['sales1'],parameter)   
        output_table, function_name, parameter = input_parser("R := select(R, (time > 50) or (qty < 30))")
        self.assertEqual('R', output_table)
        self.assertEqual('select', function_name)
        self.assertEqual(['R', '(time>50)or(qty<30)'],parameter) 
        output_table, function_name, parameter = input_parser("R := project(R, saleid, qty, pricerange)")
        self.assertEqual('R', output_table)
        self.assertEqual('project', function_name)
        self.assertEqual(['R', 'saleid', 'qty', 'pricerange'],parameter)   
        output_table, function_name, parameter = input_parser("R := avg(R1, qty) ")
        self.assertEqual('R', output_table)
        self.assertEqual('avg', function_name)
        self.assertEqual(['R1', 'qty'],parameter)   
        output_table, function_name, parameter = input_parser("R := avg(R1, qty, saleid, pricerange) ")
        self.assertEqual('R', output_table)
        self.assertEqual('avg', function_name)
        self.assertEqual(['R1', 'qty','saleid', 'pricerange'],parameter)    
        output_table, function_name, parameter = input_parser("R := sumgroup(R1, qty, time, pricerange) ")
        self.assertEqual('R', output_table)
        self.assertEqual('sumgroup', function_name)
        self.assertEqual(['R1', 'qty', 'time', 'pricerange'],parameter) 

    def test_input_parser_with_comment(self):
        output_table, function_name, parameter = input_parser("R := select(R, (time > 50) or (qty < 30)) //// select sum(qty), time, /")
        self.assertEqual('R', output_table)
        self.assertEqual('select', function_name)
        self.assertEqual(['R', '(time>50)or(qty<30)'],parameter) 

    def test_condition_parser(self):
        condition, operator = condition_parser('(R.C>5) and (S.B < 10)')
        self.assertEqual([('R.C','>','5'),('S.B','<','10')],condition)
        self.assertEqual(operator,'and')
        condition, operator = condition_parser('R.C>5')
        self.assertEqual(('R.C','>','5'),condition)
        self.assertEqual(operator,'')

if __name__ == '__main__':
    unittest.main()
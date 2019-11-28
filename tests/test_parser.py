import unittest
from database.parser import input_parser, construct_condition

class TestParser(unittest.TestCase):
    def test_input_parser(self):
        '''Test the input parser'''
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
        '''Test the input parser with comment'''
        output_table, function_name, parameter = input_parser("R := select(R, (time > 50) or (qty < 30)) //// select sum(qty), time, /")
        self.assertEqual('R', output_table)
        self.assertEqual('select', function_name)
        self.assertEqual(['R', '(time>50)or(qty<30)'],parameter) 

    def test_construct_condition(self):
        '''Test the construct condtion'''
        table = {'R1':'A_row', 'S':'B_row'}
        test_case_join = '(R1.C2 >= S.C) and (S.B < 10)'
        test_case_search = '(saleid >= 100) and (pricerange < 10)'
        test_case_arithm = '(10*R1.C2 >= S.C) and (S.B/5 < 10)'
        expect_arithm = '(10*A_row["C2"] >= B_row["C"]) and (B_row["B"]/5 < 10)'
        output_join = construct_condition(test_case_join, tableName = table)
        output_arithm = construct_condition(test_case_arithm, tableName = table)
        output_search = construct_condition(test_case_search, table = 'R')
        self.assertEqual('(A_row["C2"] >= B_row["C"]) and (B_row["B"] < 10)',output_join)
        self.assertEqual('(R["saleid"] >= 100) and (R["pricerange"] < 10)', output_search)
        self.assertEqual(expect_arithm, output_arithm)

    def test_construct_condition_with_more_than_two_condtion(self):
        '''Test the construct condtion with more than two condition'''
        table = {'R1':'A_row', 'S':'B_row'}
        test_case = '(R1.C2 >= S.C) and (S.B < 10) and (R1.salesid <= 5)'
        expected = '(A_row["C2"] >= B_row["C"]) and (B_row["B"] < 10) and (A_row["salesid"] <= 5)'
        output = construct_condition(test_case, tableName= table)
        self.assertEqual(expected, output)
    
    def test_construct_condition_with_single_equal_sign(self):
        '''Test the construct condtion with single equal sign'''
        table = {'R1':'A_row', 'S':'B_row'}
        test_case = '(R1.C2 >= S.C) and (S.B < 10) and (R1.salesid = 5)'
        expected = '(A_row["C2"] >= B_row["C"]) and (B_row["B"] < 10) and (A_row["salesid"]== 5)'
        output = construct_condition(test_case, tableName= table)
        self.assertEqual(expected, output)

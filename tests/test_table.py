import unittest
from database.table import Table

class TestTable(unittest.TestCase):
    def setUp(self):
        self.R = Table()
        self.S = Table()

    def tearDown(self):
        self.table = None

    def test_inputfile_sales1(self):
        '''Test inputfile: import sales1.csv'''
        self.R = Table.inputfromfile('sales1')
        self.assertIsNotNone(self.R.table)
        self.assertIsNotNone(self.R.table[0]['saleid'])
        self.assertIsNotNone(self.R.table[0]['itemid'])
        self.assertIsNotNone(self.R.table[0]['customerid'])
        self.assertIsNotNone(self.R.table[0]['storeid'])
        self.assertIsNotNone(self.R.table[0]['time'])
        self.assertIsNotNone(self.R.table[0]['qty'])
        self.assertIsNotNone(self.R.table[0]['pricerange'])
        self.assertEqual(self.R.table[0]['saleid'],36)
        self.assertEqual(self.R.table[0]['itemid'],14)
        self.assertEqual(self.R.table[0]['customerid'],2)
        self.assertEqual(self.R.table[0]['storeid'],38)
        self.assertEqual(self.R.table[0]['time'],49)
        self.assertEqual(self.R.table[0]['qty'],15)
        self.assertEqual(self.R.table[0]['pricerange'],'moderate')
        self.assertEqual(len(self.R.table),11)

    def test_inputfile_sales2(self):
        '''Test inputfile: import sales2.csv'''
        self.S = Table.inputfromfile('sales2')
        self.assertIsNotNone(self.S.table)
        self.assertIsNotNone(self.S.table[0]['saleid'])
        self.assertIsNotNone(self.S.table[0]['I'])
        self.assertIsNotNone(self.S.table[0]['C'])
        self.assertIsNotNone(self.S.table[0]['S'])
        self.assertIsNotNone(self.S.table[0]['T'])
        self.assertIsNotNone(self.S.table[0]['Q'])
        self.assertIsNotNone(self.S.table[0]['P'])
        self.assertEqual(self.S.table[0]['saleid'],3506)
        self.assertEqual(self.S.table[0]['I'],13517)
        self.assertEqual(self.S.table[0]['C'],16566)
        self.assertEqual(self.S.table[0]['S'],45)
        self.assertEqual(self.S.table[0]['T'],73)
        self.assertEqual(self.S.table[0]['Q'],19)
        self.assertEqual(self.S.table[0]['P'],'expensive')
        self.assertEqual(len(self.S.table),10)
    
    def test_select_with_equal_id(self):
        '''Test select with condtion: saleid = 36'''
        R = Table.inputfromfile('sales1')
        condition = 'saleid = 36'
        R1 = Table.select(R,condition)
        self.assertIsNotNone(R1.table[0])
        self.assertEqual(R1.table[0]['saleid'],36)
        self.assertEqual(R1.table[0]['itemid'],14)
        self.assertEqual(R1.table[0]['customerid'],2)
        self.assertEqual(R1.table[0]['storeid'],38)
        self.assertEqual(R1.table[0]['time'],49)
        self.assertEqual(R1.table[0]['qty'],15)
        self.assertEqual(R1.table[0]['pricerange'],'moderate')
        self.assertEqual(len(R1.table),1)

    def test_select_with_equal_pricerange(self):
        '''Test select with condtion: pricerange = 'moderate'
        '''
        R = Table.inputfromfile('sales1')
        condition = "pricerange = 'moderate'"
        R1 = Table.select(R,condition)
        for row in R1.table:
            self.assertEquals(row['pricerange'], 'moderate')

    def test_select_with_greater_equal_item_id(self):
        '''Test select with condtion: itemid >= 20'''
        R = Table.inputfromfile('sales1')
        condition = "itemid >= 20"
        R1 = Table.select(R,condition)
        for row in R1.table:
            self.assertGreaterEqual(row['itemid'], 20)

    def test_select_with_not_equal_item_id(self):
        '''Test select with condtion: itemid != 14'''
        R = Table.inputfromfile('sales1')
        condition = "itemid != 14"
        R1 = Table.select(R,condition)
        for row in R1.table:
            self.assertNotEqual(row['itemid'], 14)

    def test_select_with_multiple_condition(self):
        '''Test select with condtion: itemid >= 20 and pricerange == 'moderate'
        '''
        R = Table.inputfromfile('sales1')
        condition = "itemid >= 20 and pricerange == 'moderate'"
        R1 = Table.select(R,condition)
        for row in R1.table:
            self.assertGreaterEqual(row['itemid'], 20)
            self.assertEquals(row['pricerange'], 'moderate')

    def test_join_column_name(self):
        '''Test join wtih the output column name'''
        R = Table.inputfromfile('sales1')
        S = Table.inputfromfile('sales2')
        R1 = Table.join(R,S,'R1','S1', 'True')
        self.assertIsNotNone(R1.table)
        keyset = R1.table[0].keys()
        print(keyset)
        for key in R.table[0].keys():
            new_key = 'R1_{}'.format(key)
            self.assertTrue(new_key in keyset)
        for key in S.table[0].keys():
            new_key = 'S1_{}'.format(key)
            self.assertTrue(new_key in keyset)

    def test_join_with_same_princerage(self):
        '''Test join wtih condition: R.pricerange = S.P'''
        R = Table.inputfromfile('sales1')
        S = Table.inputfromfile('sales2')
        R1 = Table.join(R,S,'R','S', 'R.pricerange = S.P')
        self.assertIsNotNone(R1.table)
        for row in R1.table:
            self.assertIsNotNone(row['R_pricerange'], row['S_P'])
            self.assertEqual(row['R_pricerange'], row['S_P'])
        
    def test_join_with_greater(self):
        '''Test join wtih condition: R.qty >= S.Q'''
        R = Table.inputfromfile('sales1')
        S = Table.inputfromfile('sales2')
        R1 = Table.join(R,S,'R','S', 'R.qty >= S.Q')
        self.assertIsNotNone(R1.table)
        for row in R1.table:
            self.assertIsNotNone(row['R_qty'], row['S_Q'])
            self.assertGreaterEqual(row['R_qty'], row['S_Q'])

    def test_join_with_multiple_condtion(self):
        '''Test join wtih condition: (R.qty >= S.Q) and (R.pricerange = S.P)'''
        R = Table.inputfromfile('sales1')
        S = Table.inputfromfile('sales2')
        R1 = Table.join(R,S,'R','S', '(R.qty >= S.Q) and (R.pricerange = S.P)')
        self.assertIsNotNone(R1.table)
        for row in R1.table:
            self.assertIsNotNone(row['R_qty'], row['S_Q'])
            self.assertGreaterEqual(row['R_qty'], row['S_Q'])
            self.assertIsNotNone(row['R_pricerange'], row['S_P'])
            self.assertEqual(row['R_pricerange'], row['S_P'])

    def test_project_with_sales_1_and_column_saleid_itemid(self):
        '''Test projection with two columns'''
        R = Table.inputfromfile('sales1')
        R1 = Table.projection(R,'R',['saleid', 'itemid'])
        self.assertIsNotNone(R1.table)
        for row in R1.table:
            self.assertIsNotNone(row['R_saleid'])
            self.assertIsNotNone(row['R_itemid'])
            self.assertRaises(KeyError, lambda: row['R_customerid']) 
            self.assertRaises(KeyError, lambda: row['R_storeid']) 
            self.assertRaises(KeyError, lambda: row['R_time']) 
            self.assertRaises(KeyError, lambda: row['R_qty']) 
            self.assertRaises(KeyError, lambda: row['R_pricerange']) 

    def test_avg_with_sales_1_and_column_saleid(self):
        '''Test avg with: avg(saleid)'''
        R = Table.inputfromfile('sales1')
        R1 = Table.avg(R, 'saleid')
        self.assertIsNotNone(R1.table)
        sum = 0
        for row in R.table:
            sum = sum + row['saleid']
        avg = sum/len(R.table)
        for row in R1.table:
            self.assertIsNotNone(row['avg(saleid)'])
            self.assertEqual(row['avg(saleid)'], avg)

    # def test_avggroup_with_sales_1_and_column_saleid_groupby_pricerange(self):
    #     '''Test avggroup with: avgroup(R, saleid, pricerange)'''


            

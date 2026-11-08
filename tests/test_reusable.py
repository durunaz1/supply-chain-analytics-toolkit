import unittest
import pandas as pd
from src.data_quality import audit
from src.procurement import category_value
from src.suppliers import concentration, on_time_delivery
from src.inventory import abc_classification

class ToolkitTests(unittest.TestCase):
    def test_audit(self):
        self.assertEqual(audit(pd.DataFrame({'a':[1,1]}),key='a')['repeated_keys'],1)
    def test_concentration(self):
        x=pd.DataFrame({'s':['A','B'],'v':[50,50]})
        self.assertAlmostEqual(concentration(x,'s','v')['hhi'],5000)
    def test_missing_value_not_zero(self):
        x=pd.DataFrame({'cat':['a','a'],'v':[10,None]})
        self.assertEqual(category_value(x,'cat','v').iloc[0]['valued_records'],1)
    def test_no_fabricated_reliability(self):
        with self.assertRaises(ValueError):
            on_time_delivery(pd.DataFrame({'s':['a']}),'promised','actual','s')
    def test_abc(self):
        x=pd.DataFrame({'sku':['A','B','C'],'units':[80,15,5],'cost':[1,1,1]})
        self.assertEqual(abc_classification(x,'sku','units','cost').abc_class.tolist(),['A','B','C'])
if __name__=='__main__':unittest.main()

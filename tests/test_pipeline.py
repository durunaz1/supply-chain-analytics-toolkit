import unittest
import tempfile
from pathlib import Path
import pandas as pd
from src.pipeline import load_awards,category_metrics,sensitivity
class TestPipeline(unittest.TestCase):
 def test_schema_and_quality(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'input.csv'
   pd.DataFrame({'Supplier':['A','B',None],'Commodity Category':['C','C','C'],'Contract Award Amount (USD)':['100','300','100'],'Award Date':['2025-01-01','2025-01-02','2025-01-03']}).to_csv(p,index=False)
   d,q=load_awards(p)
   self.assertEqual(q['rows_usable'],2)
   r=category_metrics(d,min_awards=2).iloc[0]
   self.assertAlmostEqual(r.hhi_10000,6250)
 def test_scenario_preserves_concentration_logic(self):
  r=sensitivity(pd.Series({'A':.8,'B':.2}),fractions=[.1],new_counts=[1])
  self.assertLess(r.iloc[0].scenario_hhi,r.iloc[0].baseline_hhi)
 def test_reject_missing_fields(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'x.csv';pd.DataFrame({'foo':[1]}).to_csv(p,index=False)
   with self.assertRaises(ValueError):load_awards(p)
if __name__=='__main__':unittest.main()

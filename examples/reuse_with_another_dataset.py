"""Example of adapting the toolkit to another real dataset."""
import pandas as pd
from src.data_quality import audit
from src.procurement import category_value
from src.suppliers import concentration

# Replace this path and column names with those of your own dataset.
# df = pd.read_csv('path/to/purchase_orders.csv')
# print(audit(df, required=['vendor', 'category', 'amount']))
# print(category_value(df, category='category', value='amount'))
# print(concentration(df, supplier='vendor', value='amount')['hhi'])

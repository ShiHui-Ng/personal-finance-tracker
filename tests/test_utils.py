import sys
import os

sys.path.append(os.path.abspath("src"))

from utils import FinReview
from datetime import datetime
import pandas as pd

app = FinReview()
'''
print("Checking add transaction function...")
app.add_transaction()

print("\nChecking view option function...")
app.view_option(choice="2")
app.view_option(choice="3")
app.view_option(choice="4")

print("\nChecking view transaction by date function...")
app.view_trans_by_date()
'''

print("\nChecking monthly summary function...")
app.monthly_summary()
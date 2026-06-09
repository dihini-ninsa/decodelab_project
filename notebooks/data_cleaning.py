"""
DecodeLabs — Project 1: Data Cleaning & Preparation
Industrial Training Kit | Batch 2026
======================================================
Run this file in VS Code with: Ctrl + F5
Dataset required: Dataset_for_Data_Analytics.xlsx
"""

import pandas as pd
import re
import os

# Fix working directory
os.chdir(r'C:\Users\pc\Documents\decodelab_project')

print("=" * 55)
print("  DecodeLabs Project 1 — Data Cleaning & Preparation")
print("=" * 55)

# ═══════════════════════════════════════════════════════════
# STEP 1: LOAD THE RAW DATASET
# ═══════════════════════════════════════════════════════════
df = pd.read_excel('Dataset for Data Analytics.xlsx')
print(f"\n[LOADED] {df.shape[0]} rows × {df.shape[1]} columns")

print("\n── MISSING VALUES (Raw) ──")
print(df.isnull().sum())
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"Duplicate OrderIDs: {df.duplicated(subset='OrderID').sum()}")


# ═══════════════════════════════════════════════════════════
# STEP 2: HANDLE MISSING VALUES
# ═══════════════════════════════════════════════════════════
print("\n── PHASE 1: Missing Value Imputation ──")
missing_before = df['CouponCode'].isnull().sum()
df['CouponCode'] = df['CouponCode'].fillna('NONE')
print(f"CouponCode nulls filled: {missing_before} → 0")


# ═══════════════════════════════════════════════════════════
# STEP 3: REMOVE DUPLICATES
# ═══════════════════════════════════════════════════════════
print("\n── PHASE 2: Duplicate Removal ──")
rows_before = len(df)
df = df.drop_duplicates(subset='OrderID', keep='first')
rows_after = len(df)
print(f"Rows removed: {rows_before - rows_after}")
print(f"Remaining rows: {rows_after}")


# ═══════════════════════════════════════════════════════════
# STEP 4: FIX DATE FORMAT
# ═══════════════════════════════════════════════════════════
print("\n── PHASE 3: Date Format Standardization ──")
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
bad_dates = df[~df['Date'].str.match(r'^\d{4}-\d{2}-\d{2}$')]
print(f"Incorrectly formatted dates remaining: {len(bad_dates)}")
print("Sample dates:", df['Date'].head(5).tolist())


# ═══════════════════════════════════════════════════════════
# STEP 5: FIX NUMERIC PRECISION
# ═══════════════════════════════════════════════════════════
print("\n── Numeric Precision (2 decimals) ──")
df['UnitPrice'] = df['UnitPrice'].round(2)
df['TotalPrice'] = df['TotalPrice'].round(2)
print("UnitPrice and TotalPrice rounded to 2 decimal places.")


# ═══════════════════════════════════════════════════════════
# STEP 6: CLEAN TEXT COLUMNS
# ═══════════════════════════════════════════════════════════
print("\n── Text Standardization ──")
text_cols = ['Product', 'PaymentMethod', 'OrderStatus',
             'ReferralSource', 'CouponCode']

for col in text_cols:
    df[col] = df[col].str.strip()
    df[col] = df[col].str.title()

print("Unique Products:", df['Product'].unique().tolist())
print("Unique OrderStatus:", df['OrderStatus'].unique().tolist())
print("Unique PaymentMethod:", df['PaymentMethod'].unique().tolist())


# ═══════════════════════════════════════════════════════════
# STEP 7: VALIDATE TOTALPRICE INTEGRITY
# ═══════════════════════════════════════════════════════════
print("\n── TotalPrice Integrity Check ──")
df['_calculated'] = (df['Quantity'] * df['UnitPrice']).round(2)
mismatches = df[df['TotalPrice'] != df['_calculated']]
print(f"TotalPrice mismatches: {len(mismatches)}")
df = df.drop(columns=['_calculated'])


# ═══════════════════════════════════════════════════════════
# STEP 8: FINAL VERIFICATION
# ═══════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  FINAL VERIFICATION REPORT")
print("=" * 55)

dup_ids     = df.duplicated(subset='OrderID').sum()
bad_dates   = df[~df['Date'].str.match(r'^\d{4}-\d{2}-\d{2}$')]
total_nulls = df.isnull().sum().sum()

print(f"  Duplicate OrderIDs:        {dup_ids:<5}  ← Must be 0")
print(f"  Incorrect date formats:    {len(bad_dates):<5}  ← Must be 0")
print(f"  Total missing values:      {total_nulls:<5}  ← Must be 0")
print(f"  Final dataset shape:       {df.shape}")
print("=" * 55)

if dup_ids == 0 and len(bad_dates) == 0 and total_nulls == 0:
    print("   ALL CHECKS PASSED — Ready for Project 2!")
else:
    print("   Some checks failed. Review above.")
print("=" * 55)


# ═══════════════════════════════════════════════════════════
# STEP 9: EXPORT CLEANED DATASET
# ═══════════════════════════════════════════════════════════
df.to_excel('Cleaned_Dataset.xlsx', index=False)
print("\n[SAVED] Cleaned_Dataset.xlsx")
print("Done! ")
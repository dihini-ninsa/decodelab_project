import pandas as pd
import sqlite3

# Load Excel file into a DataFrame
df = pd.read_excel(r'C:\Users\pc\Documents\Github\decodelab_project\outputs\Cleaned_Dataset.xlsx')

# Create local SQLite database file
conn = sqlite3.connect(r'C:\Users\pc\Documents\Github\decodelab_project\outputs\orders.db')

# Load data into SQL table
df.to_sql('orders', conn, if_exists='replace', index=False)

print(" Database ready!")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print("Columns:", df.columns.tolist())

def run_query(title, sql):
    print(f"\n==================================================")
    print(f" QUERY: {title}")
    print(f"==================================================")
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False)) # index=False makes it look cleaner
    print("\n")
    return result

run_query(
    "Basic SELECT (First 10 Rows)", 
    "SELECT * FROM orders LIMIT 10"
)

# 2. WHERE — Delivered orders
run_query(
    "WHERE — Delivered Orders", 
    """
    SELECT OrderID, Product, TotalPrice, OrderStatus
    FROM orders
    WHERE OrderStatus = 'Delivered'
    LIMIT 10
    """
)

# 3. WHERE — High value orders
run_query(
    "WHERE — High Value Orders (> 2000)", 
    """
    SELECT OrderID, Product, Quantity, TotalPrice
    FROM orders
    WHERE TotalPrice > 2000
    ORDER BY TotalPrice DESC
    """
)

# 4. ORDER BY — Top 10 highest orders
run_query(
    "ORDER BY — Top 10 Highest Orders", 
    """
    SELECT OrderID, Product, TotalPrice
    FROM orders
    ORDER BY TotalPrice DESC
    LIMIT 10
    """
)

# 5. COUNT — Total orders
run_query(
    "COUNT — Total Orders", 
    "SELECT COUNT(*) AS TotalOrders FROM orders"
)

# 6. SUM and AVG — Revenue overview
run_query(
    "SUM and AVG — Revenue Overview", 
    """
    SELECT
        COUNT(*) AS TotalOrders,
        ROUND(SUM(TotalPrice), 2) AS TotalRevenue,
        ROUND(AVG(TotalPrice), 2) AS AvgOrderValue,
        ROUND(MIN(TotalPrice), 2) AS MinOrder,
        ROUND(MAX(TotalPrice), 2) AS MaxOrder
    FROM orders
    """
)

# 7. GROUP BY — Orders by status
run_query(
    "GROUP BY — Orders by Status", 
    """
    SELECT OrderStatus, COUNT(*) AS OrderCount
    FROM orders
    GROUP BY OrderStatus
    ORDER BY OrderCount DESC
    """
)

# 8. GROUP BY — Revenue by product
run_query(
    "GROUP BY — Revenue by Product", 
    """
    SELECT Product,
           COUNT(*) AS TotalOrders,
           ROUND(SUM(TotalPrice), 2) AS TotalRevenue,
           ROUND(AVG(TotalPrice), 2) AS AvgOrderValue
    FROM orders
    GROUP BY Product
    ORDER BY TotalRevenue DESC
    """
)

# 9. GROUP BY — Orders by payment method
run_query(
    "GROUP BY — Orders by Payment Method", 
    """
    SELECT PaymentMethod,
           COUNT(*) AS UsageCount,
           ROUND(SUM(TotalPrice), 2) AS TotalRevenue
    FROM orders
    GROUP BY PaymentMethod
    ORDER BY UsageCount DESC
    """
)

# 10. GROUP BY — Orders by referral source
run_query(
    "GROUP BY — Orders by Referral Source", 
    """
    SELECT ReferralSource,
           COUNT(*) AS OrderCount,
           ROUND(SUM(TotalPrice), 2) AS TotalRevenue
    FROM orders
    GROUP BY ReferralSource
    ORDER BY OrderCount DESC
    """
)

# 11. HAVING — Products with revenue over 50,000
run_query(
    "HAVING — Products with Revenue Over 50,000", 
    """
    SELECT Product, ROUND(SUM(TotalPrice), 2) AS TotalRevenue
    FROM orders
    GROUP BY Product
    HAVING SUM(TotalPrice) > 50000
    ORDER BY TotalRevenue DESC
    """
)

# 12. Combined — Cancelled and returned orders by product
run_query(
    "Combined — Cancelled and Returned Orders by Product", 
    """
    SELECT Product,
           OrderStatus,
           COUNT(*) AS Count,
           ROUND(SUM(TotalPrice), 2) AS LostRevenue
    FROM orders
    WHERE OrderStatus IN ('Cancelled', 'Returned')
    GROUP BY Product, OrderStatus
    ORDER BY LostRevenue DESC
    """
)

conn.close()
print(" Database connection closed cleanly.")
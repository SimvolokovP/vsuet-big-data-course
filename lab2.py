import pandas as pd
import numpy as np

sales = pd.DataFrame({
    'OrderID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'Product': ['Laptop', 'Phone', 'Tablet', 'Laptop', 'Phone',
                'Laptop', 'Tablet', 'Phone', 'Laptop', 'Tablet'],
    'Quantity': [1, 2, 1, 3, 1, 2, 1, 4, 1, 2],
    'Price': [50000, 30000, 20000, 50000, np.nan,
              50000, 20000, 30000, 50000, np.nan],
    'Region': ['Moscow', 'SPb', 'Kazan', 'Moscow', 'SPb',
               'Kazan', np.nan, 'SPb', 'Moscow', 'Kazan']
})

products = pd.DataFrame({
    'Product': ['Laptop', 'Phone', 'Tablet', 'Monitor'],
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Accessories'],
    'Weight_kg': [2.5, 0.2, 0.5, 3.0]
})

print("Таблица продаж:")
print(sales)
print("\nТаблица товаров:")
print(products)

# Вариант 2

# задание 1
print("--ex1--")
print(sales.groupby('Product')['Price'].agg(['min', 'max']))

# задание 2
print("--ex2--")
print(sales['Region'].value_counts())

# задание 3
print("--ex3--")
sales['Region'] = sales['Region'].fillna('Unknown')
print(sales)

# задание 4
print("--ex4--")
print(sales.sort_values(by=['Region', 'Price']))

# задание 5
print("--ex5--")
merged_df = pd.merge(sales, products, on='Product', how='left')
print(merged_df)

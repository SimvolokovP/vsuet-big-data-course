import pandas as pd
import numpy as np

data = {'ID': range(1, 11), 'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Helen', 'Ivan', 'Julia'],
    'Age': [23, 35, 29, 40, 28, 45, 32, 27, 38, 31],
    'City': ['Moscow', 'SPb', 'Moscow', 'Kazan', 'SPb', 
             'Moscow', 'SPb', 'Kazan', 'Moscow', 'SPb'],
    'Salary': [50000, 70000, 60000, 80000, 55000, 
               90000, 65000, 58000, 75000, 62000]
}

df = pd.DataFrame(data)

print(df)

# Вариант 2

# задание 1
print("--ex1--")
print(df.tail(3))

# задание 2
print("--ex2--")
print(df.iloc[[2, 4, 6]])

# задание 3
print("--ex3--")
print(df[df['City'] == 'Moscow'])

# задание 4
print("--ex4--")
print(df['Age'].max())

# задание 5
print("--ex5--")
df['Age_Category'] = df['Age'].apply(lambda x: 'Young' if x < 30 else 'Adult')
print(df)
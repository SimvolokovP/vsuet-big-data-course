import pandas as pd
import numpy as np
import glob

# Вариант 2


# задание 1
print("--ex1--")

files = glob.glob("data/orders_2024_*.csv")

df_list = []

for file in files:
    df_part = pd.read_csv(file)
    df_list.append(df_part)

if len(df_list) == 0:
    print("Файлы не найдены. Проверьте папку files и имена CSV-файлов.")
else:
    df = pd.concat(df_list, ignore_index=True)

    print("Объединенная таблица заказов:")
    print(df.head())
    print("Размер таблицы:", df.shape)


    # задание 2
    print("--ex2--")

    df['order_datetime'] = pd.to_datetime(df['order_datetime'])

    df['month'] = df['order_datetime'].dt.month

    print(df[['order_datetime', 'month']].head())


    # задание 3
    print("--ex3--")

    df['revenue'] = df['price'] * df['quantity']

    monthly_revenue = df.groupby('month')['revenue'].sum()

    print("Выручка по месяцам:")
    print(monthly_revenue)

    monthly_revenue.to_csv("monthly_revenue.csv", header=["revenue"])
    print("Результат сохранен в monthly_revenue.csv")


    # задание 4
    print("--ex4--")

    memory_before = df['status'].memory_usage(deep=True)

    print("Память до изменения:", memory_before, "байт")

    df['status'] = df['status'].astype('category')

    memory_after = df['status'].memory_usage(deep=True)

    print("Память после изменения:", memory_after, "байт")

    print("Изменение памяти:", memory_after - memory_before, "байт")

    # задание 5
    print("--ex5--")

    user_revenue = df.groupby('user_id')['revenue'].sum()

    top_10_users = user_revenue.sort_values(ascending=False).head(10)

    print("Топ-10 пользователей по суммарной выручке:")
    print(top_10_users)

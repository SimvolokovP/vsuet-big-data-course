import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

# Вариант 2

orders_files = sorted(glob.glob("data/orders_2024_*.csv"))

if len(orders_files) == 0:
    print("Файлы заказов не найдены. Проверьте папку data.")
    raise SystemExit

df_orders = pd.concat(
    [pd.read_csv(file) for file in orders_files],
    ignore_index=True
)

df_orders["order_datetime"] = pd.to_datetime(df_orders["order_datetime"])
df_orders["weekday"] = df_orders["order_datetime"].dt.day_name()

# задание 1
print("--ex1--")

plt.figure(figsize=(8, 5))
plt.hist(df_orders["quantity"].dropna(), bins=20, edgecolor="black")
plt.title("Распределение количества товаров в заказах")
plt.xlabel("Количество товаров (quantity)")
plt.ylabel("Частота")
plt.tight_layout()
plt.show()

# задание 2
print("--ex2--")

quantity_mean = df_orders["quantity"].mean()
quantity_median = df_orders["quantity"].median()

print(f"Среднее количество товаров: {quantity_mean:.2f}")
print(f"Медианное количество товаров: {quantity_median:.2f}")

# задание 3
print("--ex3--")

weekday_order = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

plt.figure(figsize=(9, 5))
sns.countplot(data=df_orders, x="weekday", order=weekday_order)
plt.title("Количество строк заказов по дням недели")
plt.xlabel("День недели")
plt.ylabel("Количество строк заказов")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# задание 4
print("--ex4--")

weekday_counts = df_orders["weekday"].value_counts()
max_weekday = weekday_counts.idxmax()
max_orders = weekday_counts.max()

print("Количество строк заказов по дням недели:")
print(weekday_counts)
print(f"Больше всего строк заказов в день {max_weekday}: {max_orders}")

# задание 5
print("--ex5--")

print("Аналитический вывод:")
print(f"Среднее количество товаров в строке заказа: {quantity_mean:.2f}.")
print(f"Медианное количество товаров: {quantity_median:.2f}.")

if quantity_mean > quantity_median:
    print("Среднее выше медианы: строки с большим количеством товаров могут смещать среднее вверх.")
elif quantity_mean < quantity_median:
    print("Среднее ниже медианы: распределение может быть смещено в сторону малых значений.")
else:
    print("Среднее совпадает с медианой: заметного расхождения этих показателей нет.")

print(f"Наибольшая активность по числу строк заказов приходится на {max_weekday} ({max_orders}).")
print("Вывод относится к числу строк в исходных CSV; один заказ может содержать несколько строк.")

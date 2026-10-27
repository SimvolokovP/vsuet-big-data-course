import pandas as pd
import numpy as np
import glob
import os

# Вариант 2


print("--ex1--")

orders_files = sorted(glob.glob("data/orders_2024_*.csv"))

if len(orders_files) == 0:
    print("Файлы заказов не найдены. Проверьте папку files.")
    raise SystemExit

df_orders = pd.concat(
    [pd.read_csv(file) for file in orders_files],
    ignore_index=True
)

events_records_file = "data/events_records.json"
events_lines_file = "data/events_lines.json"

events_list = []

if os.path.exists(events_records_file):
    df_events_records = pd.read_json(events_records_file, orient="records")
    events_list.append(df_events_records)

if os.path.exists(events_lines_file):
    df_events_lines = pd.read_json(events_lines_file, lines=True)
    events_list.append(df_events_lines)

if len(events_list) == 0:
    print("Файлы событий не найдены. Проверьте папку files.")
    raise SystemExit

df_events = pd.concat(events_list, ignore_index=True)

duplicates_orders = df_orders.duplicated(
    subset=["order_id", "user_id", "product_id", "order_datetime"]
)

duplicates_events = df_events.duplicated(
    subset=["event_id", "user_id", "event_time", "event_type", "page"]
)

print("Количество дублирующихся строк в заказах:", duplicates_orders.sum())
print("Количество дублирующихся строк в событиях:", duplicates_events.sum())


print("--ex2--")

orders_rows_before = len(df_orders)
events_rows_before = len(df_events)

df_orders_clean = df_orders[~duplicates_orders].copy()
df_events_clean = df_events[~duplicates_events].copy()

orders_rows_after = len(df_orders_clean)
events_rows_after = len(df_events_clean)

print("Заказы до удаления:", orders_rows_before)
print("Заказы после удаления:", orders_rows_after)
print("События до удаления:", events_rows_before)
print("События после удаления:", events_rows_after)

print("--ex3--")

orders_reduction = (
    (orders_rows_before - orders_rows_after) / orders_rows_before * 100
    if orders_rows_before > 0 else 0
)

events_reduction = (
    (events_rows_before - events_rows_after) / events_rows_before * 100
    if events_rows_before > 0 else 0
)

orders_memory_before = df_orders.memory_usage(deep=True).sum() / 1024**2
orders_memory_after = df_orders_clean.memory_usage(deep=True).sum() / 1024**2

events_memory_before = df_events.memory_usage(deep=True).sum() / 1024**2
events_memory_after = df_events_clean.memory_usage(deep=True).sum() / 1024**2

print(f"Уменьшение количества строк в заказах: {orders_reduction:.2f}%")
print(f"Уменьшение количества строк в событиях: {events_reduction:.2f}%")

print(f"Память заказов до очистки: {orders_memory_before:.2f} MB")
print(f"Память заказов после очистки: {orders_memory_after:.2f} MB")

print(f"Память событий до очистки: {events_memory_before:.2f} MB")
print(f"Память событий после очистки: {events_memory_after:.2f} MB")

df_orders_clean.to_csv("orders_clean.csv", index=False)
df_events_clean.to_csv("events_clean.csv", index=False)

print("Очищенные данные сохранены в orders_clean.csv и events_clean.csv")

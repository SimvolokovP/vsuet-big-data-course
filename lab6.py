import pandas as pd
import numpy as np
import glob

# Вариант 2

# задание 1
print("--ex1--")

orders_files = sorted(glob.glob("data/orders_2024_*.csv"))

if len(orders_files) == 0:
    print("Файлы заказов не найдены. Проверьте папку data.")
    raise SystemExit

df_orders = pd.concat(
    [pd.read_csv(file) for file in orders_files],
    ignore_index=True
)

sheets = pd.read_excel("data/products.xlsx", sheet_name=["products", "categories"])
df_products = sheets["products"]
df_categories = sheets["categories"]

df_prod_full = df_products.merge(
    df_categories,
    on="category_id",
    how="left"
)

df_prod_full = df_prod_full.drop(columns=["category_name_x"])
df_prod_full = df_prod_full.rename(
    columns={"category_name_y": "category_name"}
)

df_orders_prod = df_orders.merge(
    df_prod_full,
    on="product_id",
    how="left"
)

df_orders_prod["revenue"] = (
    df_orders_prod["price"] * df_orders_prod["quantity"]
)

print("Столбцы после объединения:")
print(df_orders_prod.columns.tolist())

revenue_pivot = pd.pivot_table(
    df_orders_prod,
    values="revenue",
    index="category_name",
    columns="status",
    aggfunc="sum",
    fill_value=0
)

print("Выручка по категориям и статусам:")
print(revenue_pivot)

# задание 2
print("--ex2--")

# Доля отменённой выручки в общей выручке категории
category_total = revenue_pivot.sum(axis=1)
cancelled_revenue = revenue_pivot.get("cancelled", pd.Series(0, index=revenue_pivot.index))
cancel_share = cancelled_revenue.div(category_total.where(category_total != 0)).fillna(0)

category_risk = pd.DataFrame({
    "cancelled_revenue": cancelled_revenue,
    "total_revenue": category_total,
    "cancel_share": cancel_share
})

print("Доля отменённой выручки по категориям:")
print(category_risk)

# задание 3
print("--ex3--")

# Пороги риска: менее 10% — низкий, 10–30% — средний, более 30% — высокий.
category_risk["risk_level"] = np.select(
    [category_risk["cancel_share"] < 0.10,
     category_risk["cancel_share"] <= 0.30],
    ["низкий", "средний"],
    default="высокий"
)

print("Категории с уровнем риска отмен:")
print(category_risk)

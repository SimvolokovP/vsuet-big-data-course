import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns

# Вариант 2

orders_files = sorted(glob.glob('data/orders_2024_*.csv'))

if len(orders_files) == 0:
    print('Файлы заказов не найдены. Проверьте папку data.')
    raise SystemExit

df_orders = pd.concat(
    [pd.read_csv(file) for file in orders_files],
    ignore_index=True
)

df_orders['price'] = pd.to_numeric(df_orders['price'], errors='coerce')
prices = df_orders['price'].dropna()

if prices.empty:
    print('В столбце price нет числовых значений для анализа.')
    raise SystemExit

# задание 1
print('--ex1--')
plt.figure(figsize=(9, 5))
sns.histplot(prices, bins=30, kde=True)
plt.title('Распределение цен (price)')
plt.xlabel('Цена')
plt.ylabel('Количество позиций')
plt.tight_layout()
plt.show()

# задание 2
print('--ex2--')
mean_price = prices.mean()
median_price = prices.median()
print(f'Средняя цена: {mean_price:.2f}')
print(f'Медианная цена: {median_price:.2f}')
print(f'Разница среднего и медианы: {mean_price - median_price:.2f}')

# задание 3
print('--ex3--')
q1 = prices.quantile(0.25)
q3 = prices.quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df_orders[(df_orders['price'] < lower) | (df_orders['price'] > upper)].copy()
print(f'Нижняя граница IQR: {lower:.2f}')
print(f'Верхняя граница IQR: {upper:.2f}')
print(f'Количество выбросов: {len(outliers)}')
print(f'Доля выбросов: {len(outliers) / len(prices) * 100:.2f}%')
print('Примеры выбросов:')
print(outliers[['order_id', 'price']].head(10))

# задание 4
print('--ex4--')
prices_without_outliers = prices[(prices >= lower) & (prices <= upper)]
mean_without_outliers = prices_without_outliers.mean()
print(f'Средняя цена с выбросами: {mean_price:.2f}')
print(f'Средняя цена без выбросов: {mean_without_outliers:.2f}')
print(f'Изменение средней цены: {mean_price - mean_without_outliers:.2f}')
if mean_price > mean_without_outliers:
    print('Выбросы повышают среднюю цену. Медиана обычно устойчивее к крайним значениям.')
elif mean_price < mean_without_outliers:
    print('Выбросы понижают среднюю цену. Медиана обычно устойчивее к крайним значениям.')
else:
    print('Удаление найденных выбросов не изменило среднюю цену.')

# задание 5
print('--ex5--')
print(f'Проанализировано {len(prices)} ценовых значений.')
print(f'Средняя цена составляет {mean_price:.2f}, медиана — {median_price:.2f}.')
print(f'Методом IQR найдено {len(outliers)} выбросов ({len(outliers) / len(prices) * 100:.2f}%).')
if mean_price > median_price:
    print('Среднее выше медианы: распределение может иметь правостороннюю асимметрию.')
elif mean_price < median_price:
    print('Среднее ниже медианы: распределение может иметь левостороннюю асимметрию.')
else:
    print('Среднее и медиана совпадают.')
print('При оценке типичной цены полезно учитывать медиану и влияние выбросов, а не только среднее.')

import pandas as pd
import numpy as np

# Вариант 2

# задание 1
print("--ex1--")

df_events_records = pd.read_json("data/events_records.json", orient="records")
df_events_lines = pd.read_json("data/events_lines.json", lines=True)

df_events = pd.concat(
    [df_events_records, df_events_lines],
    ignore_index=True
)

df_events["event_time"] = pd.to_datetime(df_events["event_time"])

events_ts = df_events.set_index("event_time").sort_index()
events_hourly = events_ts["event_id"].resample("h").count().to_frame("events_count")

print("Количество событий по часам:")
print(events_hourly.head(10))


# задание 2
print("--ex2--")

events_hourly["events_rolling_3h"] = (
    events_hourly["events_count"]
    .rolling(window=3, min_periods=1)
    .sum()
)

print("Количество событий и скользящее окно за 3 часа:")
print(events_hourly.head(10))


# задание 3
print("--ex3--")

df_events["event_hour"] = df_events["event_time"].dt.floor("h")

user_hourly = (
    df_events.groupby(["user_id", "event_hour"])["event_id"]
    .count()
    .reset_index(name="events_count")
)

top_user_hour = user_hourly.sort_values(
    "events_count",
    ascending=False
).head(1)

print("Пользователь с наибольшим количеством событий за один час:")
print(top_user_hour)

CREATE DATABASE IF NOT EXISTS weather_db;

CREATE TABLE IF NOT EXISTS weather_db.weather_hourly (
    city String,
    datetime DateTime,
    temperature Float32,
    precipitation Float32,
    wind_speed Float32,
    wind_direction Float32
) ENGINE = MergeTree()
ORDER BY (city, datetime);

CREATE TABLE IF NOT EXISTS weather_db.weather_daily (
    city String,
    date Date,
    min_temp Float32,
    max_temp Float32,
    avg_temp Float32,
    precipitation_sum Float32
) ENGINE = MergeTree()
ORDER BY (city, date);
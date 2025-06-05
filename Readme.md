# Module 10 : SQLAlchemy Challenge


In this module, I work with real-world climate data from a SQLite database. The goal is to explore, analyze, and visualize weather patterns to gain insights into precipitation, temperature, and station activity.

## Dependencies

1. SQLAlchemy – to interact with the climate database using Python ORM queries
2. Pandas – to manipulate and analyze structured data
3. Matplotlib – to visualize your findings

## Usage

* Part 1 : Analyze and Explote the Climate Data `Climate_Analysis/climate.ipynb`

* Part 2 : Designing Climate App, Run `Climate_Analysis/app.py`

Browse :[http://127.0.0.1:5000](http://127.0.0.1:5000)

## API Guide

Here’s a **concise API usage guide** (like you'd find in a `README.md`) based on your `api_v1` Blueprint routes for the Climate App API:

---

# 🌦️ Climate App API – v1.0

Base URL: `/api/v1.0`

## 📘 Overview

This RESTful API provides climate data including precipitation levels, temperature observations, and station info from Hawaii’s climate dataset. It supports querying historical data for analysis and visualization purposes.

---

## 📌 Endpoints

### `/api/v1.0/`

**Description:** API base route.
**Method:** `GET`
**Response:**

```json
{
  "message": "climate app api version 1"
}
```

---

### `/api/v1.0/precipitation`

**Description:** Returns daily precipitation data for the last year from the most recent record.
**Method:** `GET`
**Response:**

```json
{
  "2016-08-23": 0.0,
  "2016-08-24": 0.08,
  ...
}
```

---

###  `/api/v1.0/stations`

**Description:** Returns a dictionary of station IDs and their names.
**Method:** `GET`
**Response:**

```json
{
  "USC00519397": "WAIKIKI 717.2, HI US",
  "USC00513117": "KANEOHE 838.1, HI US",
  ...
}
```

---

###  `/api/v1.0/tobs`

**Description:** Returns temperature observations for the most active station over the last year.
**Method:** `GET`
**Response:**

```json
{
  "2016-08-23": 77.0,
  "2016-08-24": 80.0,
  ...
}
```

---

### `/api/v1.0/<start>`

**Description:** Returns min, max, and average temperature observations from a given start date (inclusive) to the end of the dataset.
**Method:** `GET`
**Path Params:**

* `start` (format: `YYYY-MM-DD`)
  **Example:** `/api/v1.0/2017-01-01`
  **Response:**

```json
{
  "min_tobs": 62.0,
  "max_tobs": 82.0,
  "avg_tobs": 69.5
}
```

---

### `/api/v1.0/<start>/<end>`

**Description:** Returns min, max, and average temperature observations between a start and end date (inclusive).
**Method:** `GET`
**Path Params:**

* `start` (format: `YYYY-MM-DD`)
* `end` (format: `YYYY-MM-DD`)
  **Example:** `/api/v1.0/2017-01-01/2017-01-07`
  **Response:**

```json
{
  "min_tobs": 63.0,
  "max_tobs": 81.0,
  "avg_tobs": 70.1
}
```
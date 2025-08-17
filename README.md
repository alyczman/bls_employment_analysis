# BLS Employment Trend Analysis

## Learning Goals
 - Gain experience with the Bureau of Labour Statistics (BLS) API to pull employment data
 - Further understanding of Pandas and Python Syntax
 - Begin utilization of UV as a package manager
 - Set the stage for development of ETL project for forcasting

## Languages Used

| Rank | Languages |
|-----:|-----------|
|     2| Python    |
|     3| SQL       |

## Tools Used

| Tools | Languages |
|-----:|-----------|
|     1| VSCode    |
|     2| PostGres  |


## Overview:

This personal project is aimed at building an end-to-end data engineering pipeline using publicly available BLS data via its public API. The project stages are as follows:

- Pull series, year, period, and value data from the public api ranging from 2015 to 2020 and (for now) convert the data into pandas dataframes for use in                 visualizations using matplotlib and plotly.
- The next iteration will aims to upload the data frames to a Postgres SQL database and create a basic db schema to support a powerbi or streamlit dashboard.
- After that, goal is to add in additional data validation and batch scheduling via an ETL tool and Apache Airflow
- Finally, maybe do some simple forcasting for a little ML twist. 

## Introduction

Welcome to the WeServe Call Center Data Engineering Project. This project aims to analyze and derive key performance indicators (KPIs) from the call center data of WeServe, a call service agency that outsources customer service personnel to various companies. By cleaning, transforming, and storing the data in a structured format, we seek to provide valuable insights into the activities of call center agents and enhance the management's understanding of agent performance and customer service quality.

### Project Overview

- **Objective**: The primary objective of this project is to create a comprehensive analysis of call center operations and generate KPIs to measure agent performance and customer service quality.
- **Scope**: This project covers data cleaning, transformation, and the creation of KPI tables. We also document the ETL (Extract, Transform, Load) process and recommend potential areas for future work.

### Data Source

The dataset used in this project originates from WeServe's call center operations. It is a CSV file which includes information on customer calls, call durations, agent details, complaint topics, call statuses, and resolution durations. This data forms the foundation for our analysis and KPI calculations.

### Key Tasks and Accomplishments

This project encompasses several key tasks and accomplishments, including:

- Cleaning and refining the raw call center data to address data quality issues and ensure accuracy.
- Transforming the dataset to create KPIs, such as measuring the number of calls resolved vs. received, calls received vs. assigned/resolved, and call duration per agent.
- Storing the cleaned and transformed data in a PostgreSQL database for structured analysis.
- Documenting the ETL process, data cleaning, and KPI calculations for transparency and future reference.

In the sections that follow, we provide a detailed account of the data cleaning, transformation, and KPI calculation processes. We also present the database schema, ETL automation, challenges faced, potential future work, and a summary of findings.

By the end of this project, we aim to equip WeServe with a robust data infrastructure and analytical tools to facilitate data-driven decision-making, enhance customer service, and optimize agent performance.



### 2. Data Cleaning

The data cleaning process involved preparing the raw data for subsequent analysis and KPI calculation. A copy of the two datasets was created call_details_copy and call_log_copy. Several data quality issues were identified and addressed. Here are the key steps taken during data cleaning:

#### 2.1. Handling Missing Data

- Identified and recorded missing values in the dataset.
- For columns with missing values, various approaches were employed:
   - Numeric columns: Filled missing values with 0 for the resolution_duration_in_hours.
   - Filled missing values in assigned_to with the corresponding agent_id
   - alligned the fonts in status 
   - rename headers for the two csv files
   - adjust the in 'inbound' in call_type and status to a consistent case

#### 2.2. Data Type Conversions

- Ensured that data types for each column were consistent with their content.
- Converted data types as follows:
   - Converted 'assigned_to' to integer data type from float.
   - Converted call_id to int from object

#### 2.3. Data Validation and Correction

- Conducted data validation to identify and correct data integrity issues.
- Identified and corrected inconsistencies in the 'callType' and 'call_ended_by_agent' columns, ensuring uniformity.

#### 2.4. Data Quality Report

- Generated a summary report highlighting data quality issues, actions taken, and the resulting dataset.
- Documented the cleaned dataset, which served as the basis for subsequent KPI calculations.

The data cleaning process improved the dataset's quality and readiness for KPI calculation and analysis.


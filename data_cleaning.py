# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 10:21:47 2021

@author: hangu
"""
#scrapping errors were not resolved. Use provided data from KenJee
#import glassdoor_scrapper as gs

import pandas as pd

#This will open a new chrome window and start scrapping
df = pd.read_csv("https://raw.githubusercontent.com/PlayingNumbers/ds_salary_proj/master/glassdoor_jobs.csv")

# 1. salary parsing

#create column hourly to see if the employer has a per hour rate
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
#create column to see if employer provided the salary
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

df = df[df['Salary Estimate']!= '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary + df.max_salary)/2

# 2. company name text only

# remove 3 chars from the end to take the rating away from name
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis = 1)

# 3. state field

df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df.job_state.value_counts()

# 4. age of company

#check whether the job is at the headquaters
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)
# get age of company
df['age'] = df.Founded.apply(lambda x: x if x<1 else 2020 - x)

# 5. parsing of job description (python, etc.)

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

#r studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

#spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower()else 0)
df.spark.value_counts()

#aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower()else 0)
df.aws.value_counts()

#excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower()else 0)
df.excel.value_counts()

df_out = df.drop(['Unnamed: 0'], axis = 1)

df_out.to_csv('salary_data_clean.csv', index = False)

pd.read_csv('salary_data_clean.csv')
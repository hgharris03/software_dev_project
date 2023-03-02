#!/usr/bin/env python
# coding: utf-8

# # Insights on Vehicles for Sale

# I will be building an app for users to quickly make comparisons on vehicles for sale and look through a list of options to buy from. This notebook is mainly used for data validation and basic analysis. 

# Install modules and import libraries

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


#pip install pipenv


# In[3]:


#pip install streamlit


# In[4]:


import streamlit as st
#from matplotlib import pyplot as plt


# In[5]:


cars = pd.read_csv('vehicles_us.csv')

#display(cars.info())
#display(cars.head())


# In[6]:


cars['date_posted'] = pd.to_datetime(cars['date_posted'], format = '%Y-%m-%d')
#print('min:', cars['date_posted'].min(), 
#      'max:', cars['date_posted'].max())


# I will be adding a column to categorize the age of the car. The dataset appears to be taken from 2019 so I will set the current year to 2019 to line up with timeline of the dataset.

# In[7]:


cars['age'] = 2019 - cars['model_year']

def age_category(x):
    if x< 5: return '0 - 5'
    elif x>=5 and x<10: return '5 - 10'
    elif x>=10 and x<20: return '10 - 20' 
    elif x>=20: return '>20'
    else: return 'Not Specified' 
cars['age_category'] = cars['age'].apply(age_category)



# I will be looking in more detail of the dataframe to understand the missing values and data better. 

# In[8]:


#display(cars['price'].describe())


# It is unlikely that a car will sell for $1, especially when some of these vehicles are in good condition. I've deciced to drop these rows so price comparisons and analysis will be more accurate. 

# In[9]:


cars = cars[cars['price'] != 1]
#print(cars.info())
#print(cars['price'].describe())


# In[10]:


#print(cars['cylinders'].describe())
#print(cars['cylinders'].unique())


# The median and the mean cylinder the vehicles have is 6 so I will fill the empty values with 6.

# In[11]:


cars['cylinders'] = cars['cylinders'].fillna(6)
#print(cars['cylinders'].describe())
#print(cars['cylinders'].unique())


# In[12]:


#print(cars['odometer'].describe())
cars['odometer'] = cars['odometer'].fillna(114160.5)


# In[13]:


#print(cars['odometer'].describe())


# In[14]:


#print(cars['paint_color'].unique())
cars['paint_color'] = cars['paint_color'].fillna('none specified')


# In[15]:


#print(cars['paint_color'].unique())


# In[16]:


#print(cars['is_4wd'].unique())


# The column for 4wd is 1 for yes, the rest of the values are blank. I am going to use 'yes' or 'no' for better usibility. 

# In[17]:


cars['is_4wd'] = cars['is_4wd'].replace({1:'yes'})
cars['is_4wd'] = cars['is_4wd'].fillna('no')
#print(cars['is_4wd'].unique())


# In[18]:


#print(cars.columns)
cars['model_year'] = cars['model_year'].round(0)
#display(cars.head())


# In[19]:


#print(cars.info())


# Finding the model of car with the most ads. 

# In[20]:


model_cars_sorted = cars.groupby('model')['price'].count().sort_values(ascending = False)
#print(model_cars_sorted)


# In[21]:


#model_cars_sorted.head(25).plot(kind = 'bar', xlabel = 'Car Model', ylabel = 'Count', title = 'Models with the most ads')
#plt.show()


# Since Ford -150 is the most popular car, I am going to do further analysis on this model. 

# In[24]:


#ford_f150 = cars[cars['model'] == 'ford f-150']
#ford_f150['age'].hist(bins = 100)
#plt.title('Age distribution of Ford F150')
#plt.xticks([0,10,20,30,40,50,60,70,80,90,100])
#plt.show()


# In[25]:


#ford_f150_age = ford_f150.groupby('age_category').median().sort_values('age')
#display(ford_f150_age)


# As expected the price of the trucks decrease as the age increased. A histogram will show the distribution of the age Ford f-150 trucks for sale. While the table above is not comprihensive of all categories in the dataset it quickly summarizes competitive prices at each age category. This information is useful when car shopping so I will include it in the web app with the option to pick a car model.  

# In[52]:
st.header('Market of used cars in US')
st.write("""
#### Filter the data below median info grouped by age by manufacturer """)

model_choice = cars['model'].unique()
choice_mod = st.selectbox('Select model:', model_choice)
model_choice_age = cars[cars['model'] == choice_mod].groupby('age_category').median().sort_values('age')
st.table(model_choice_age)



# In[42]:


import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly"


# In[43]:


list_for_hist = ['condition', 'transmission', 'type', 'paint_color']

choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)

fig1 = px.histogram(cars, x = 'price', color = choice_for_hist)

fig1.update_layout(title = '<b> Split of price by {}</b>'.format(choice_for_hist))

st.plotly_chart(fig1)


# In[44]:


#fig1


# In[46]:


st.write(""" 
##### How price is affected by odometer, transmission or number of cylinders in the ads
""")

list_for_scatter = ['age_category', 'odometer', 'transmission', 'cylinders']

choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)

fig2 = px.scatter(cars, x = 'price', y = choice_for_scatter, hover_data = ['model_year'])

fig2.update_layout(title= "<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2)


# In[47]:


#fig2


# In[48]:
st.write("""
#### Filter the data below to see the ads by manufacturer """)

manufacturer_choice = cars['model'].unique()
make_choice_mod = st.selectbox('Select model for ads:', manufacturer_choice)

condition_choice = cars['condition'].unique()
make_condition = st.selectbox('Select condition: ', condition_choice)


# In[49]:


min_day_list, max_day_list = int(cars['days_listed'].min()), int(cars['days_listed'].max())

days_range = st.slider('Days Listed', value=(min_day_list, max_day_list), min_value = min_day_list, max_value = max_day_list)


# In[50]:


actual_range = list(range(days_range[0], days_range[1] +1))


# In[51]:


filtered_type = cars[(cars.model == make_choice_mod) & (cars['days_listed'].isin(list(actual_range))) & (cars.condition == make_condition)]


# In[37]:


st.table(filtered_type)


# # Conclusion

# The dataset included vehicle advertisements collected starting from May 2018 through April 2019. 
# The most popular vehicle model to sell is Ford f150. A general trend is as the age of the vehicles increase the price decreases. 
# 

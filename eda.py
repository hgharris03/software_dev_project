#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


#pip install pipenv


# In[3]:


#pip install streamlit


# In[4]:


import streamlit as st


# In[6]:


cars = pd.read_csv('vehicles_us.csv')

display(cars.info())


# In[7]:


print(cars.columns)


# In[8]:


st.header('Market of used cars. Original data')
st.write("""
#### Filter the data below to see the ads by manufacturer """)
show_new_cars = st.checkbox('Include new cars from dealers')


# In[9]:


show_new_cars


# In[10]:


if not show_new_cars:
    cars = cars[cars.condition != 'new']


# In[11]:


manufacturer_choice = cars['model'].unique()
make_choice_mod = st.selectbox('Select model:', manufacturer_choice)


# In[12]:


make_choice_mod


# In[13]:


min_price, max_price = int(cars['price'].min()), int(cars['price'].max())

price_range = st.slider('Price Range', value=(min_price, max_price), min_value = min_price, max_value = max_price)


# In[14]:


price_range


# In[15]:


actual_range = list(range(price_range[0], price_range[1] +1))


# In[16]:


filtered_type = cars[(cars.model == make_choice_mod) & (cars.model_year.isin(list(actual_range)))]
st.table(filtered_type)


# In[17]:


cars


# In[18]:


import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly"


# In[19]:


list_for_hist = ['condition', 'transmission', 'type', 'color']

choice_for_hist = st.selectbox('Split for price distribution', list_for_hist)

fig1 = px.histogram(cars, x = 'price', color = choice_for_hist)

fig1.update_layout(title = '<b> Split of price by {}</b>'.format(choice_for_hist))

st.plotly_chart(fig1)


# In[20]:


fig1


# In[21]:


cars['age'] = 2022 - cars['model_year']

def age_category(x):
    if x< 5: return '<5'
    elif x>5 and x<10: return '5-10'
    elif x>10 and x<20: return '10-20' 
    else: return '>20' 
cars['age_category'] = cars['age'].apply(age_category)


# In[22]:


cars['age_category'].head()


# In[23]:


st.write(""" 
##### Now let's check how price is affected by odometer, transmission or number of cylinders in the ads
""")

list_for_scatter = ['odometer', 'transmission', 'cylinders']

choice_for_scatter = st.selectbox('Price dependency on ', list_for_scatter)

fig2 = px.scatter(cars, x = 'price', y = choice_for_scatter, hover_data = ['model_year'])

fig2.update_layout(title= "<b> Price vs {}</b>".format(choice_for_scatter))
st.plotly_chart(fig2)


# In[24]:


fig2


# In[ ]:
git config --global user.email "hgharris03@gmail.com"
git config --global user.name "hgharris03"




# %%

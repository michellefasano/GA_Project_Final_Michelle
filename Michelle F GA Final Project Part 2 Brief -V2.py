
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np

# Read the data into a DataFrame
path = 'skill_and_wages4.csv'
skills = pd.read_csv(path)



# In[3]:


skills.head()
skills.dtypes
#check out data
#median annual wage is not a float, will need to change this


# In[4]:


wage = skills.loc[:,'wage']

#tried wage.replace(['>=$208,000'],['208000'],inplace=True)
#then wage.astype('float64',errors='ignore')
#this still wouldn't go to numeric - so examined which are non numeric


# In[5]:


skills.loc[:,'wage']= wage
skills.head()


# In[6]:


skills.nunique()
skills.describe()


# In[ ]:





# In[7]:


#explore which are non numeric

wage_not_num = skills.loc[:,'wage'].str.isnumeric() ==False

skills.loc[wage_not_num,:]

#its only a few rows....going to just remove


# In[8]:


wage_num = skills.loc[:,'wage'].str.isnumeric()

skills = skills.loc[wage_num,:]


# In[9]:


skills.describe(include= ['object'])

skills.shape

#1091 > 1080 so these rows were indeed removed 


# In[10]:


skills.wage = pd.to_numeric(skills['wage'])
#yay! wage is now numeric, might have been able to use this way all along

skills.dtypes


# In[15]:


fig, ax = plt.subplots()
skills.plot(kind='scatter',x='active_listening',y='wage',ax=ax);
#as an example, active listening has a slight correlation with wage

fig, ax = plt.subplots()

skills.loc[:,'wage'].hist(bins=15,ax=ax);


# In[12]:



axes = pd.plotting.scatter_matrix(skills, figsize=(15,15));

#would like to see this bigger to help me choose which skills are most correlated


# In[13]:


skills.isnull().sum()
#no null values so that is good


# In[14]:


#next steps:

#determine which skills are most correlated with wage, may have to combine skills to make new features
#perhaps take out wage bands that are not relevant to this analysis (over 80k)
#still a wide range of wage values for when a given skill is zero - this will throw off data, need to firgure out how to deal with this
#could also look at abilities or knowledge instead of skills


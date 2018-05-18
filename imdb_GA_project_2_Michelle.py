
# coding: utf-8

# <img src="http://imgur.com/1ZcRyrc.png" style="float: left; margin: 20px; height: 55px">
# 
# # Project 2: Analyzing IMDb Data
# 
# _Author: Kevin Markham (DC)_
# 
# ---

# For project two, you will complete a serious of exercises exploring movie rating data from IMDb.
# 
# For these exercises, you will be conducting basic exploratory data analysis on IMDB's movie data, looking to answer such questions as:
# 
# What is the average rating per genre?
# How many different actors are in a movie?
# 
# This process will help you practice your data analysis skills while becoming comfortable with Pandas.

# ## Basic level

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# #### Read in 'imdb_1000.csv' and store it in a DataFrame named movies.

# In[2]:


movies = pd.read_csv('./data/imdb_1000.csv')
movies.head()


# #### Check the number of rows and columns.

# In[3]:


# Answer:
movies.shape


# #### Check the data type of each column.

# In[4]:


# Answer:
movies.dtypes


# #### Calculate the average movie duration.

# In[30]:


# Answer:
movies.duration.mean()


# #### Sort the DataFrame by duration to find the shortest and longest movies.

# In[28]:


# Answer:
#get top ten then botton ten
movies.sort_values(['duration']).head(10)

movies.sort_values(['duration'],ascending=False).head(10)


# #### Create a histogram of duration, choosing an "appropriate" number of bins.

# In[29]:


# Answer:
#create figure then select just duration to apply hist. played around with bins, 6 looked good
fig, ax = plt.subplots()
movies.loc[:,'duration'].hist(ax=ax,bins=6);


# #### Use a box plot to display that same data.

# In[8]:


# Answer:
#changed to box and .plot
fig, ax = plt.subplots()
movies.loc[:,'duration'].plot(kind='box',ax=ax);


# ## Intermediate level

# #### Count how many movies have each of the content ratings.

# In[9]:


# Answer:
#select just content ratings to do the value count
movies_ratings = movies.loc[:,'content_rating'].value_counts()
movies_ratings


# #### Use a visualization to display that same data, including a title and x and y labels.

# In[10]:


# Answer:
#bar h is best here since its categorical data
fig, ax = plt.subplots()
movies_ratings.plot(kind='barh',ax=ax)


# #### Convert the following content ratings to "UNRATED": NOT RATED, APPROVED, PASSED, GP.

# In[11]:


# Answer:
#replace a full list of values with the new value and check by showing head
movies.replace(['NOT RATED', 'APPROVED', 'PASSED', 'GP'],'UNRATED').head(10)


# #### Convert the following content ratings to "NC-17": X, TV-MA.

# In[12]:


# Answer:
#same
movies.replace(['X','TV-MA'],'NC-17').head(10)


# #### Count the number of missing values in each column.

# In[13]:


# Answer:
#can sum boolean series
movies.isnull().sum()


# #### If there are missing values: examine them, then fill them in with "reasonable" values.

# In[14]:


# Answer:
#examine by creating a boolean series of missing values then filtering with it
null_movies = movies.isnull().loc[:,"content_rating"]
movies.loc[null_movies,:]
movies.replace('NaN','R').head(10)
#replacing with "R" -  the most common value


# #### Calculate the average star rating for movies 2 hours or longer, and compare that with the average star rating for movies shorter than 2 hours.

# In[15]:


# Answer:
#create a new column then assign values to it based on formulas - have to translate hours to minutes
movies['length'] = '< 2 hours'
movies['length'][movies['duration']<120] = '< 2 hours'
movies['length'][movies['duration']>=120] = '>= 2 hours'

movies.groupby('length')['star_rating'].mean()
#looks like the rating is higher for longer movies, by a little)


# #### Use a visualization to detect whether there is a relationship between duration and star rating.

# In[16]:


# Answer:
#scatter plot is best for relationship detection, no relationship really
fig, ax = plt.subplots()
movies.plot.scatter('star_rating','duration',ax=ax);


# #### Calculate the average duration for each genre.

# In[17]:


# Answer:
#group by genrea and get the mean of duration
movies.groupby('genre')['duration'].mean()


# ## Advanced level

# #### Visualize the relationship between content rating and duration.

# In[18]:


# Answer:
#do a plot on top of a group by
fig, ax = plt.subplots()
movies.groupby('content_rating')['duration'].mean().sort_values().plot(kind='barh',ax=ax)



# #### Determine the top rated movie (by star rating) for each genre.

# In[19]:


# Answer:
movies.groupby(['genre','title'])['star_rating'].max()

movies.groupby(['genre'])['star_rating','title'].max()


# #### Check if there are multiple movies with the same title, and if so, determine if they are actually duplicates.

# In[20]:


# Answer:
#see if all titles have 1 count or more - 4 had more so can manually type those out and filter by that boolean series
movies.loc[:,'title'].value_counts()
dup_list = movies.loc[:,'title'].isin(['The Girl with the Dragton Tattoo', 'Les Miserables','Dracula','True Grit'])

movies.loc[dup_list,:]
#they are not duplicates
movies[movies.duplicated()] #check with this function


# #### Calculate the average star rating for each genre, but only include genres with at least 10 movies
# 

# #### Option 1: manually create a list of relevant genres, then filter using that list

# In[21]:


# Answer:
#manually typed out based on a values count that showed me the relevant genres
top_genres = movies.loc[:,'genre'].isin(['Action','Adventure','Animation','Biography','Comedy','Crime','Drama','Horror', 'Mystery'])
movies.loc[top_genres,:].groupby('genre')['star_rating'].mean()


# #### Option 2: automatically create a list of relevant genres by saving the value_counts and then filtering

# In[22]:


# Answer:
#use dictionary keys to get an auto list
top_genres2 = movies.loc[:,'genre'].value_counts() > 10
top_genres3 = dict(top_genres2[top_genres2 != False]).keys()

top_genres4 = movies.loc[:,'genre'].isin(top_genres3)
movies.loc[top_genres4,:].groupby('genre')['star_rating'].mean()


# #### Option 3: calculate the average star rating for all genres, then filter using a boolean Series

# In[23]:


# Answer:

movies.groupby('genre')['star_rating'].agg(['mean']).loc[top_genres2,:]


# #### Option 4: aggregate by count and mean, then filter using the count

# In[24]:


# Answer:
#filter the group by by a series that is the same shape as the group by
top_list = movies.groupby('genre')['star_rating'].agg(['count','mean']).loc[:,'count']>10
movies.groupby('genre')['star_rating'].agg(['count','mean']).loc[top_list,'mean']


# ## Bonus

# #### Figure out something "interesting" using the actors data!

# In[25]:


#create a function that will split out a list into seperate rows and duplicate info in other columns
def splitDataFrameList(df,target_column,separator):
    ''' df = dataframe to split,
    target_column = the column containing the values to split
    separator = the symbol used to perform the split
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
    '''
    def splitListToRows(row,row_accumulator,target_column,separator):
        split_row = row[target_column].split(separator)
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)
    new_rows = []
    df.apply(splitListToRows,axis=1,args = (new_rows,target_column,separator))
    new_df = pd.DataFrame(new_rows)
    return new_df


# In[31]:


#run new function
#then get only the top 20 movies to make the rest simpler
#then clean the actors list data to remove certain charactesr
#then get the avg rating by actor and visualize
top_movies = splitDataFrameList(movies,'actors_list',",").sort_values('star_rating',ascending=False).head(20)

top_movies.actors_list = top_movies.loc[:,'actors_list'].str.replace(']','').str.replace('[','').str.replace('u','')
best_actors = top_movies.groupby('actors_list')['star_rating'].agg(['mean','count']).sort_values('mean',ascending=False).head(10)
best_actors


# In[32]:


fig, ax = plt.subplots()
best_actors.loc[:,:].plot(kind='barh',ax=ax)
#tim robbins is the highest but all the top ten only have one movie - so is that really saying much?


# -*- coding: utf-8 -*-
"""Assignment2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tYgXd89jJOv8ZuWiQgl9haUF4Bm8zSE-

# Assignment 1

Andrew ID: aarushis

Sources: This helped me understand how to go about solving this problem https://github.com/junjiedong/Zillow-Kaggle/blob/master/explanatory.ipynb
"""

import numpy as np
import matplotlib.pyplot as plt
import sklearn
import pickle
import pandas as pd
import seaborn as sns 
import graphviz
import pickle

# Reading all files
t16=pd.read_csv('train_2016.csv')
t17=pd.read_csv('train_2017.csv')
p16 = pd.read_csv('properties_2016.csv')
p17 = pd.read_csv('properties_2017.csv')

"""We merge the datasets based on parcelId as properties has more properties than the log error files."""

merged_df = pd.merge(p16, t16, on='parcelid')
p16=merged_df
merged_df = pd.merge(p17, t17, on='parcelid')
p17=merged_df
x=pd.concat([p16,p17])
print(p16.shape)
print(p17.shape)
print(x.shape)

# Looking at the property data now - 58 features
#p16 = pd.read_csv('properties_2016.csv')
print(p16.shape)
p16.head()

"""Trying to Visualize"""

#Visualization
# check which features have the most null values
plt.figure(figsize=(20,35))
x.notnull().mean().sort_values().plot(kind = 'bar')

"""Looking at data types for all fields"""

print(x.dtypes)

"""Display the distribution of three numeric fields.

"""

# i have chosen 
# 1. poolcnt
# 2. yearbuilt
# 3. bedroomcnt
data=x['bedroomcnt']
plt.hist(data,bins=30)
plt.xlabel('Bedroom Count')
plt.ylabel('Frequency')
plt.title('Histogram of Feature Values')
plt.show()

data=x['yearbuilt']
plt.hist(data,bins=30)
plt.xlabel('Year Built')
plt.ylabel('Frequency')
plt.title('Histogram of Feature Values')
plt.show()

data=x['poolcnt']
plt.hist(data,bins=30)
plt.xlabel('Unit Count')
plt.ylabel('Frequency')
plt.title('Histogram of Feature Values')
plt.show()

data=x['logerror']
plt.hist(data,bins=30)
plt.xlabel('logerror')
plt.ylabel('Frequency')
plt.title('Histogram of Feature Values')
plt.show()

# properties with no pool count should have 0 
x.poolcnt.fillna(0,inplace = True)
data=x['poolcnt']
plt.hist(data,bins=30)
plt.xlabel('Unit Count')
plt.ylabel('Frequency')
plt.title('Histogram of Feature Values')
plt.show()

#seeing the average of logerror
average = x['logerror'].mean()
print(average)

# Checking if there is any column with no nan values except parcelId.
null_counts = x.isnull().sum()
print(null_counts.sort_values())

# finding the correlation between all features
correlation_matrix = x.corr()
# Get the absolute correlation coefficients for each feature pair
abs_corrs = correlation_matrix.abs()

# Find the feature pairs with a correlation of 1
corr_pairs = abs_corrs[abs_corrs==1.0].stack().reset_index().values.tolist()

# Print the correlated features with correlation of 1
print("Features with a correlation of 1:")
for pair in corr_pairs:
    feature1, feature2, corr = pair
    print(f"{feature1} and {feature2} with a correlation of {corr}")

#dropping some columns with high correlation and redundancy
#x.drop('finishedsquarefeet12', axis=1, inplace=True)
#x.drop('finishedsquarefeet13', axis=1, inplace=True)
#x.drop('finishedsquarefeet6', axis=1, inplace=True)

# Let's check the unique values for "decktypeid"
for col_name in x.columns:
  print(x[col_name].value_counts())

"""Data Cleaning based on the above outputs"""

x.poolcnt.fillna(0,inplace = True)
x.poolsizesum.fillna(0,inplace = True)
x.pooltypeid10.fillna(0,inplace = True)
x.pooltypeid2.fillna(0,inplace = True)
x.pooltypeid7.fillna(0,inplace = True)
x.fireplacecnt.fillna(0,inplace = True)
x.yardbuildingsqft17.fillna(0,inplace = True)
x.yardbuildingsqft26.fillna(0,inplace = True)
x.basementsqft.fillna(0,inplace = True)

#nan tax flags mean not due for this property
x.taxdelinquencyflag.fillna(0,inplace = True)
x.taxdelinquencyflag.replace(to_replace = 'Y', value = 1,inplace = True)
#no hot tubs-nan means 0
x.hashottuborspa.fillna(0,inplace = True)
#no decks-nan means 0
x.decktypeid.fillna(0,inplace = True)





# imputing based on data dictionary
x.heatingorsystemtypeid.fillna(13,inplace = True)
x.airconditioningtypeid.fillna(5,inplace = True)
x.architecturalstyletypeid.fillna(19,inplace = True)
x.typeconstructiontypeid.fillna(14,inplace = True)

#filling the remaing fields with the most occuring value
propertylandusetypeid = x['propertylandusetypeid'].value_counts().idxmax()
x['propertylandusetypeid'] = x['propertylandusetypeid'].fillna(propertylandusetypeid)

x['bathroomcnt'] = x['bathroomcnt'].fillna(x['bathroomcnt'].value_counts().idxmax())

x['bedroomcnt'] = x['bedroomcnt'].fillna(x['bedroomcnt'].value_counts().idxmax())

x['assessmentyear'] = x['assessmentyear'].fillna(x['assessmentyear'].value_counts().idxmax())

x['fips'] = x['fips'].fillna(x['fips'].value_counts().idxmax())

x['propertycountylandusecode'] = x['propertycountylandusecode'].fillna(x['propertycountylandusecode'].value_counts().idxmax())

x['rawcensustractandblock'] = x['rawcensustractandblock'].fillna(x['rawcensustractandblock'].value_counts().idxmax())

x['roomcnt'] = x['roomcnt'].fillna(x['roomcnt'].value_counts().idxmax())

x['longitude'] = x['longitude'].fillna(x['longitude'].value_counts().idxmax())

x['latitude'] = x['latitude'].fillna(x['latitude'].value_counts().idxmax())

x['regionidzip'] = x['regionidzip'].fillna(x['regionidzip'].value_counts().idxmax())

x['yearbuilt'] = x['yearbuilt'].fillna(x['yearbuilt'].value_counts().idxmax())

x['unitcnt'] = x['unitcnt'].fillna(x['unitcnt'].value_counts().idxmax())

x['propertyzoningdesc'] = x['propertyzoningdesc'].fillna(x['propertyzoningdesc'].value_counts().idxmax())

x['buildingqualitytypeid'] = x['buildingqualitytypeid'].fillna(x['buildingqualitytypeid'].value_counts().idxmax())

x['calculatedbathnbr'] = x['calculatedbathnbr'].fillna(x['calculatedbathnbr'].value_counts().idxmax())

x['censustractandblock'] = x['censustractandblock'].fillna(x['censustractandblock'].value_counts().idxmax())
#can fill this value with the average as it is monetary/area value
x['taxvaluedollarcnt'].fillna((x['taxvaluedollarcnt'].mean()), inplace=True)
x['calculatedfinishedsquarefeet'].fillna((x['calculatedfinishedsquarefeet'].mean()), inplace=True)
x['taxamount'].fillna((x['taxamount'].mean()), inplace=True)
x['lotsizesquarefeet'].fillna((x['lotsizesquarefeet'].mean()), inplace=True)

#structuretaxvaluedollarcnt will be 0 for lots with no structure
x.structuretaxvaluedollarcnt.fillna(0,inplace = True)
x.landtaxvaluedollarcnt.fillna(0,inplace = True)
x.landtaxvaluedollarcnt.fillna(0,inplace = True)

#assuming nan means 0 garages
x.garagecarcnt.fillna(0,inplace = True)
x.garagetotalsqft.fillna(0,inplace = True)

# minimum stories will be 1 (ground floor)
x.numberofstories.fillna(1,inplace = True)

#dropping other columns
x.drop('fullbathcnt', axis=1, inplace=True)
#location info is redundant
x.drop('regionidcounty', axis=1, inplace=True)
x.drop('regionidcity', axis=1, inplace=True)
x.drop('regionidneighborhood', axis=1, inplace=True)

x.drop('finishedsquarefeet12', axis=1, inplace=True)
x.drop('finishedsquarefeet50', axis=1, inplace=True)
x.drop('finishedsquarefeet15', axis=1, inplace=True)
x.drop('finishedsquarefeet13', axis=1, inplace=True)
x.drop('finishedsquarefeet6', axis=1, inplace=True)
x.drop('threequarterbathnbr', axis=1, inplace=True)
x.drop('finishedfloor1squarefeet', axis=1, inplace=True)
x.drop('fireplaceflag', axis=1, inplace=True)
x.drop('storytypeid', axis=1, inplace=True)
x.drop('buildingclasstypeid', axis=1, inplace=True)



#year for which unpaid taxes were due does not matter
x.drop('taxdelinquencyyear', axis=1, inplace=True)

x['hashottuborspa'] = x['hashottuborspa'].astype(int)
x['taxdelinquencyflag'] = x['taxdelinquencyflag'].astype(int)

# Checking if there is any column with nan values.
null_counts = x.isnull().sum()
print(null_counts.sort_values())

#identified from above
#x.basementsqft.fillna(0,inplace = True)

# finding the correlation between all features
#correlation_matrix = p16.corr()
#plt.figure(figsize=(200, 200))
# Create heatmap of correlation matrix
#sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

# Show the plot
#plt.show()

"""Splitting data"""

from sklearn.model_selection import train_test_split
x.drop(['propertyzoningdesc','propertycountylandusecode'],axis=1,inplace = True)
train, test = train_test_split(x, test_size=0.49, random_state=42)
train_y=pd.DataFrame(train['logerror'])
test_y=pd.DataFrame(test['logerror'])
train.drop('logerror', axis=1, inplace=True)
test.drop('logerror', axis=1, inplace=True)
train.drop('transactiondate', axis=1, inplace=True)
test.drop('transactiondate', axis=1, inplace=True)
print(train.shape)
print(train_y.shape)
print(test.shape)
print(test_y.shape)
print(train.dtypes)

"""Modelling"""

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder


# create a logistic regression model and fit it to the training data
linreg = LinearRegression()
linreg.fit(train, train_y)

# make predictions on the testing set
y_pred = linreg.predict(test)

# calculate the mean absolute error (MAE) and mean squared error (MSE)
mae = mean_absolute_error(test_y, y_pred)
mse = mean_squared_error(test_y, y_pred)
print("Liner Reg.")
print("MAE:", mae)
print("MSE:", mse)

with open('zillow.model.pkl', 'wb') as f:
    # Write the model to the file using pickle.dump()
    pickle.dump(linreg, f)

# Initialize a Gradient Boosting regressor with a small learning rate
gbm = GradientBoostingRegressor(learning_rate=0.0015, n_estimators=100, loss='ls', random_state=42,max_depth=10)
gbm.fit(train, train_y)
# make predictions on the testing set
y_pred2 = gbm.predict(test)

# calculate the mean absolute error (MAE) and mean squared error (MSE)
mae = mean_absolute_error(test_y, y_pred2)
mse = mean_squared_error(test_y, y_pred2)

#giving result below baseline
# create a logistic regression model and fit it to the training data
#dt = DecisionTreeRegressor()
#dt.fit(train, train_y)

# make predictions on the testing set
#y_pred = dt.predict(test)

# calculate the mean absolute error (MAE) and mean squared error (MSE)
#mae = mean_absolute_error(test_y, y_pred)
#mse = mean_squared_error(test_y, y_pred)

print("Gradient")
print("MAE:", mae)
print("MSE:", mse)

"""# New section"""
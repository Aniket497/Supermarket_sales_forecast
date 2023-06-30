import pandas as pd
import numpy as np
from pandas import Series, DataFrame

# Pie Chart/ Bar graph
import matplotlib.pyplot as plt
superstore = pd.read_csv('ssf.csv')
superstore.head()
# Drop the unnecessary columns
superstore_clean = superstore.drop(['Row ID','Customer ID','Country','Product ID','Ship Date'],axis=1)

# Break down the date into a month and year
superstore_clean['Year'] = superstore_clean['Order Date'].astype(str).str[6:10]
superstore_clean['Month'] = superstore_clean['Order Date'].astype(str).str[3:5]
superstore_clean.drop(columns =["Order Date"], inplace = True)

superstore_clean.head()
# Converting the data to prep it for correlation table

# Creating a new dataframe for us add and alter columns
superstore_clean_corr_df = superstore_clean.copy()

# Dropping columns to large to turn into categorical
superstore_clean_corr = superstore_clean_corr_df.drop(['Order ID','Customer Name','City','State','Sub-Category','Product Name'], axis = 1)

# Ship Mode:
superstore_clean_corr['Ship Mode'].unique()
superstore_clean_corr['Ship Mode'] = superstore_clean_corr['Ship Mode'].replace(["Same Day","First Class","Second Class","Standard Class"],["1","2","3","4"])

# Segment
superstore_segment = pd.get_dummies(superstore_clean_corr['Segment'])
superstore_clean_corr = pd.concat([superstore_clean_corr,superstore_segment], axis = 1)
superstore_clean_corr = superstore_clean_corr.drop(['Segment'],axis =1)

# Region
superstore_region = pd.get_dummies(superstore_clean_corr['Region'])
superstore_clean_corr = pd.concat([superstore_clean_corr,superstore_segment], axis = 1)
superstore_clean_corr = superstore_clean_corr.drop(['Region'],axis =1)

# Category
superstore_category = pd.get_dummies(superstore_clean_corr['Category'])
superstore_clean_corr = pd.concat([superstore_clean_corr,superstore_segment], axis = 1)
superstore_clean_corr = superstore_clean_corr.drop(['Category'],axis =1)

# Correlation table
superstore_clean_corr.corr()
#This is what we are focusing on
dataframe = superstore_clean['Ship Mode']
#the if statement is to ensure that there are no more than 5 values shown at the piechart and everything else will be clustered into 'other'
if dataframe.nunique() >= 5:
    #This creates the top 5 highest values
    dataframe_value_counts_top5 = dataframe.value_counts().nlargest(5)
    #This just counts how many are left after removing the top 5
    remaining = dataframe.nunique() - 5
    #This clusters the remaning counts into a seperate dataset
    other = dataframe.value_counts().nsmallest(remaining)
    #create a dataframe from the previous two datasets and sum together the 'other' dataset
    df_top5 = pd.DataFrame(dataframe_value_counts_top5)
    df_other = pd.DataFrame([other.sum()],columns = ['Sub-Category'],index = ['Other'])
    #combine the datasets
    df_top5_other = pd.concat([df_top5,df_other])
    df_top5_other_1 = pd.DataFrame(df_top5_other)
    df_top5_other_2 = df_top5_other_1.reset_index().rename(columns={'index': 'Unique', 'Sub-Category': 'Value Counts'})
    #this is the x axis and the y axis for the pie chart
    dataframe_unique = df_top5_other_2['Unique'].unique()
    dataframe_value_counts = df_top5_other_2['Value Counts']
else:
    dataframe_unique = dataframe.unique()
    dataframe_value_counts = dataframe.value_counts()
#this counts the amount of values that will have to be pulled for a color scheme, so you dont have to manually imput it
dataframe_unique_num = len(dataframe_unique)
cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]
#this multiplies the number of unique values by what kind of explosion you want
explode = [0.05] * dataframe_unique_num

plt.pie(dataframe_value_counts,
        explode=explode,
        labels=dataframe_unique,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

plt.axis('equal')
plt.show()
# this is the dataset we are focusing on
dataframe = superstore.groupby(['Ship Mode'])['Sales'].sum().sort_values()

# this provides the top 10 highest value
if dataframe.nunique() >= 10:
    dataframe = dataframe.nlargest(10)

df_dataframe = pd.DataFrame(dataframe).reset_index()
x_axis = df_dataframe.iloc[:, 0].unique()
y_axis = df_dataframe.iloc[:, 1]
dataframe_unique_num = len(x_axis)
cmap = plt.get_cmap('Paired')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]

fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(x_axis, y_axis, color=colors, zorder=3)

ax.grid(color='lightgrey', linestyle='-', linewidth=2, axis='both', alpha=0.2)

# this adds numbers to each bar
for i, v in enumerate(y_axis):
    ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')

plt.show()
# Determining gender based on customers name
# Dividing the "Customer Name" by first and last name

# Creating a second dataframe dedicated to altering
# superstore_clean_gender = superstore_clean.copy()

# new = superstore_clean_gender["Customer Name"].str.split(" ", n = 1, expand = True)

# making separate first name column from new data frame
# superstore_clean_gender["First Name"]= new[0]

# making separate last name column from new data frame
# superstore_clean_gender["Last Name"]= new[1]

# Dropping old Name columns
# superstore_clean_gender.drop(columns =["Customer Name"], inplace = True)

# df display
# superstore_clean_gender.head()

# There was no modern library to read genders from name
#Determing returning customer based on Order ID
superstore_clean_vc = superstore_clean['Order ID'].value_counts()
superstore_clean_df = pd.DataFrame(superstore_clean_vc)

superstore_clean_df_single = pd.DataFrame(superstore_clean_df[superstore_clean_df['Order ID'] == 1].count())
superstore_clean_df_repeat = pd.DataFrame(superstore_clean_df[superstore_clean_df['Order ID'] > 1].count())

superstore_clean_df_piechart = pd.concat([superstore_clean_df_single,superstore_clean_df_repeat])
superstore_clean_df_piechart.plot(kind = "pie",
                                  subplots = True,
                                  explode = (0.01,0.01),
                                  colors = ['gold','yellowgreen'],
                                  labels = ['Single Purchases','Returning Customers'],
                                  startangle = 90,
                                  autopct = '%1.1f%%',
                                  title='Types of Customers based on Purchasing Consistency',
                                  legend = None)
#Total Sales per Types of Customer
#Try to do the Gender Guesser either through a standard library or create a dictionary
#Types of Categories found in both types of customers
#A percent distribution of types of customers
dataframe = superstore_clean['Segment']

if dataframe.nunique() >= 5:
    dataframe_value_counts_top5 = dataframe.value_counts().nlargest(5)
    remaining = dataframe.nunique() - 5
    other = dataframe.value_counts().nsmallest(remaining)
    df_top5 = pd.DataFrame(dataframe_value_counts_top5)
    df_other = pd.DataFrame([other.sum()],columns = ['Sub-Category'],index = ['Other'])
    df_top5_other = pd.concat([df_top5,df_other])
    df_top5_other_1 = pd.DataFrame(df_top5_other)
    df_top5_other_2 = df_top5_other_1.reset_index().rename(columns={'index': 'Unique', 'Sub-Category': 'Value Counts'})
    dataframe_unique = df_top5_other_2['Unique'].unique()
    dataframe_value_counts = df_top5_other_2['Value Counts']
else:
    dataframe_unique = dataframe.unique()
    dataframe_value_counts = dataframe.value_counts()

dataframe_unique_num = len(dataframe_unique)
cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]
explode = [0.05] * dataframe_unique_num

plt.pie(dataframe_value_counts,
        explode=explode,
        labels=dataframe_unique,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

plt.axis('equal')
plt.show()
#Categories found within each Segment
#Total Sales covered by Consumer Type
# this is the dataset we are focusing on
dataframe = superstore.groupby(['Segment'])['Sales'].sum().sort_values()

# this provides the top 10 highest value
if dataframe.nunique() >= 10:
    dataframe = dataframe.nlargest(10)

df_dataframe = pd.DataFrame(dataframe).reset_index()
x_axis = df_dataframe.iloc[:, 0].unique()
y_axis = df_dataframe.iloc[:, 1]
dataframe_unique_num = len(x_axis)
cmap = plt.get_cmap('Paired')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]

fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(x_axis, y_axis, color=colors, zorder=3)

ax.grid(color='lightgrey', linestyle='-', linewidth=2, axis='both', alpha=0.2)

# this adds numbers to each bar
for i, v in enumerate(y_axis):
    ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')

plt.show()
#Total Sales per city
# this is the dataset we are focusing on
dataframe = superstore.groupby(['City'])['Sales'].sum().sort_values()

# this provides the top 10 highest value
if dataframe.nunique() >= 10:
    dataframe = dataframe.nlargest(10)

df_dataframe = pd.DataFrame(dataframe).reset_index()
x_axis = df_dataframe.iloc[:, 0].unique()
y_axis = df_dataframe.iloc[:, 1]
dataframe_unique_num = len(x_axis)
cmap = plt.get_cmap('Paired')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]

fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(x_axis, y_axis, color=colors, zorder=3)

ax.grid(color='lightgrey', linestyle='-', linewidth=2, axis='both', alpha=0.2)

# this adds numbers to each bar
for i, v in enumerate(y_axis):
    ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')

plt.show()
# this is the dataset we are focusing on
dataframe = superstore.groupby(['State'])['Sales'].sum().sort_values()

# this provides the top 10 highest value
if dataframe.nunique() >= 10:
    dataframe = dataframe.nlargest(10)

df_dataframe = pd.DataFrame(dataframe).reset_index()
x_axis = df_dataframe.iloc[:, 0].unique()
y_axis = df_dataframe.iloc[:, 1]
dataframe_unique_num = len(x_axis)
cmap = plt.get_cmap('Paired')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]

fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(x_axis, y_axis, color=colors, zorder=3)

ax.grid(color='lightgrey', linestyle='-', linewidth=2, axis='both', alpha=0.2)

# this adds numbers to each bar
for i, v in enumerate(y_axis):
    ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')

plt.show()
dataframe = superstore_clean['Region']

if dataframe.nunique() >= 5:
    dataframe_value_counts_top5 = dataframe.value_counts().nlargest(5)
    remaining = dataframe.nunique() - 5
    other = dataframe.value_counts().nsmallest(remaining)
    df_top5 = pd.DataFrame(dataframe_value_counts_top5)
    df_other = pd.DataFrame([other.sum()],columns = ['Sub-Category'],index = ['Other'])
    df_top5_other = pd.concat([df_top5,df_other])
    df_top5_other_1 = pd.DataFrame(df_top5_other)
    df_top5_other_2 = df_top5_other_1.reset_index().rename(columns={'index': 'Unique', 'Sub-Category': 'Value Counts'})
    dataframe_unique = df_top5_other_2['Unique'].unique()
    dataframe_value_counts = df_top5_other_2['Value Counts']
else:
    dataframe_unique = dataframe.unique()
    dataframe_value_counts = dataframe.value_counts()

dataframe_unique_num = len(dataframe_unique)
cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]
explode = [0.05] * dataframe_unique_num

plt.pie(dataframe_value_counts,
        explode=explode,
        labels=dataframe_unique,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

plt.axis('equal')
plt.show()
# this is the dataset we are focusing on
dataframe = superstore.groupby(['Region'])['Sales'].sum().sort_values()

# this provides the top 10 highest value
if dataframe.nunique() >= 10:
    dataframe = dataframe.nlargest(10)

df_dataframe = pd.DataFrame(dataframe).reset_index()
x_axis = df_dataframe.iloc[:, 0].unique()
y_axis = df_dataframe.iloc[:, 1]
dataframe_unique_num = len(x_axis)
cmap = plt.get_cmap('Paired')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]

fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(x_axis, y_axis, color=colors, zorder=3)

ax.grid(color='lightgrey', linestyle='-', linewidth=2, axis='both', alpha=0.2)

# this adds numbers to each bar
for i, v in enumerate(y_axis):
    ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')

plt.show()
dataframe = superstore_clean['Category']

if dataframe.nunique() >= 5:
    dataframe_value_counts_top5 = dataframe.value_counts().nlargest(5)
    remaining = dataframe.nunique() - 5
    other = dataframe.value_counts().nsmallest(remaining)
    df_top5 = pd.DataFrame(dataframe_value_counts_top5)
    df_other = pd.DataFrame([other.sum()],columns = ['Sub-Category'],index = ['Other'])
    df_top5_other = pd.concat([df_top5,df_other])
    df_top5_other_1 = pd.DataFrame(df_top5_other)
    df_top5_other_2 = df_top5_other_1.reset_index().rename(columns={'index': 'Unique', 'Sub-Category': 'Value Counts'})
    dataframe_unique = df_top5_other_2['Unique'].unique()
    dataframe_value_counts = df_top5_other_2['Value Counts']
else:
    dataframe_unique = dataframe.unique()
    dataframe_value_counts = dataframe.value_counts()

dataframe_unique_num = len(dataframe_unique)
cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]
explode = [0.05] * dataframe_unique_num

plt.pie(dataframe_value_counts,
        explode=explode,
        labels=dataframe_unique,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

plt.axis('equal')
plt.show()
# this is the dataset we are focusing on
dataframe = superstore.groupby(['Category'])['Sales'].sum().sort_values()

# this provides the top 10 highest value
if dataframe.nunique() >= 10:
    dataframe = dataframe.nlargest(10)

df_dataframe = pd.DataFrame(dataframe).reset_index()
x_axis = df_dataframe.iloc[:, 0].unique()
y_axis = df_dataframe.iloc[:, 1]
dataframe_unique_num = len(x_axis)
cmap = plt.get_cmap('Paired')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]

fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(x_axis, y_axis, color=colors, zorder=3)

ax.grid(color='lightgrey', linestyle='-', linewidth=2, axis='both', alpha=0.2)

# this adds numbers to each bar
for i, v in enumerate(y_axis):
    ax.text(i, v, str(round(v, 2)), ha='center', va='bottom')

plt.show()
superstore_clean_category_furniture = superstore_clean[superstore_clean['Category'] == 'Furniture']
superstore_clean_category_officesupplies = superstore_clean[superstore_clean['Category'] == 'Office Supplies']
superstore_clean_category_technology = superstore_clean[superstore_clean['Category'] == 'Technology']
dataframe = superstore_clean_category_furniture['Sub-Category']

if dataframe.nunique() >= 5:
    dataframe_value_counts_top5 = dataframe.value_counts().nlargest(5)
    remaining = dataframe.nunique() - 5
    other = dataframe.value_counts().nsmallest(remaining)
    df_top5 = pd.DataFrame(dataframe_value_counts_top5)
    df_other = pd.DataFrame([other.sum()],columns = ['Sub-Category'],index = ['Other'])
    df_top5_other = pd.concat([df_top5,df_other])
    df_top5_other_1 = pd.DataFrame(df_top5_other)
    df_top5_other_2 = df_top5_other_1.reset_index().rename(columns={'index': 'Unique', 'Sub-Category': 'Value Counts'})
    dataframe_unique = df_top5_other_2['Unique'].unique()
    dataframe_value_counts = df_top5_other_2['Value Counts']
else:
    dataframe_unique = dataframe.unique()
    dataframe_value_counts = dataframe.value_counts()

dataframe_unique_num = len(dataframe_unique)
cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]
explode = [0.05] * dataframe_unique_num

plt.pie(dataframe_value_counts,
        explode=explode,
        labels=dataframe_unique,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

plt.axis('equal')
plt.show()
dataframe = superstore_clean_category_technology['Sub-Category']

if dataframe.nunique() >= 5:
    dataframe_value_counts_top5 = dataframe.value_counts().nlargest(5)
    remaining = dataframe.nunique() - 5
    other = dataframe.value_counts().nsmallest(remaining)
    df_top5 = pd.DataFrame(dataframe_value_counts_top5)
    df_other = pd.DataFrame([other.sum()],columns = ['Sub-Category'],index = ['Other'])
    df_top5_other = pd.concat([df_top5,df_other])
    df_top5_other_1 = pd.DataFrame(df_top5_other)
    df_top5_other_2 = df_top5_other_1.reset_index().rename(columns={'index': 'Unique', 'Sub-Category': 'Value Counts'})
    dataframe_unique = df_top5_other_2['Unique'].unique()
    dataframe_value_counts = df_top5_other_2['Value Counts']
else:
    dataframe_unique = dataframe.unique()
    dataframe_value_counts = dataframe.value_counts()

dataframe_unique_num = len(dataframe_unique)
cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]
explode = [0.05] * dataframe_unique_num

plt.pie(dataframe_value_counts,
        explode=explode,
        labels=dataframe_unique,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

plt.axis('equal')
plt.show()
dataframe = superstore_clean_category_officesupplies['Sub-Category']

if dataframe.nunique() >= 5:
    dataframe_value_counts_top5 = dataframe.value_counts().nlargest(5)
    remaining = dataframe.nunique() - 5
    other = dataframe.value_counts().nsmallest(remaining)
    df_top5 = pd.DataFrame(dataframe_value_counts_top5)
    df_other = pd.DataFrame([other.sum()],columns = ['Sub-Category'],index = ['Other'])
    df_top5_other = pd.concat([df_top5,df_other])
    df_top5_other_1 = pd.DataFrame(df_top5_other)
    df_top5_other_2 = df_top5_other_1.reset_index().rename(columns={'index': 'Unique', 'Sub-Category': 'Value Counts'})
    dataframe_unique = df_top5_other_2['Unique'].unique()
    dataframe_value_counts = df_top5_other_2['Value Counts']
else:
    dataframe_unique = dataframe.unique()
    dataframe_value_counts = dataframe.value_counts()

dataframe_unique_num = len(dataframe_unique)
cmap = plt.get_cmap('coolwarm')
colors = [cmap(i) for i in np.linspace(0, 1, dataframe_unique_num)]
explode = [0.05] * dataframe_unique_num

plt.pie(dataframe_value_counts,
        explode=explode,
        labels=dataframe_unique,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90)

plt.axis('equal')
plt.show()
superstore_clean_sales = superstore_clean[['Year','Month','Sales']].groupby(['Year','Month']).sum()
superstore_clean_year = superstore_clean[['Year','Sales']].groupby(['Year']).sum()
superstore_clean_month = superstore_clean[['Month','Sales']].groupby(['Month']).sum()

superstore_clean_year.plot(kind='bar',
                           figsize = (5,5),
                           subplots = True,
                           legend = False,
                           width = 0.5,
                           title = ('Total Sales Annually'))

superstore_clean_month.plot(kind='bar',
                           figsize = (5,5),
                           subplots = True,
                           legend = False,
                           width = 0.5,
                           title = ('Total Sales Monthly'))

superstore_clean_sales.plot(kind='line',
                           figsize = (15,5),
                            linewidth = 2,
                           subplots = True,
                           legend = False,
                           title = ('Total Sales'))
plt.xticks(range(len(superstore_clean_sales.index)), superstore_clean_sales.index, rotation=90, fontsize=8)

plt.tight_layout()

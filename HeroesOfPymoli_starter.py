#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[2]:


player_demographics = purchase_data.loc[:, ["SN", "Gender", "Age"]]
player_demographics = player_demographics.drop_duplicates()
num_players = player_demographics.count()[0]
pd.DataFrame({"Total Number of Players": [num_players]})


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


# Caliculation to obtain number of unique items

average_item_price = purchase_data["Price"].mean()
total_purchase_value = purchase_data["Price"].sum()
purchase_count = purchase_data["Price"].count()
item_count = len(purchase_data["Item ID"].unique())
summary_table = pd.DataFrame({"Number of Unique Items": [item_count],
                              "Average Price" : [average_item_price],
                              "Number of Purchases":[purchase_count],
                              "Total Revenue":[total_purchase_value]})
summary_table = summary_table.round(2)

#Display the summary data frame

summary_table["Average Price"] = summary_table["Average Price"].map("${:,.2f}".format)
summary_table["Number of Purchases"] = summary_table["Number of Purchases"].map("{:,}".format)
summary_table["Total Revenue"] = summary_table["Total Revenue"].map("${:,.2f}".format)
summary_table = summary_table.loc[:, ["Number of Unique Items","Average Price","Number of Purchases",
                              "Total Revenue"]]
summary_table


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


#calculate the number od percentage by gender

gender_demographics_total = player_demographics["Gender"].value_counts()
gender_demographics_percent = gender_demographics_total/num_players
gender_demographics = pd.DataFrame({
    "Total Count": gender_demographics_total,
    "Percentage of Players": gender_demographics_percent
})

#Display the summary data frame

gender_demographics["Percentage of Players"] = gender_demographics["Percentage of Players"].map("{:,.2%}".format)
gender_demographics


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[5]:


#run calculation
gender_purchase_total = purchase_data.groupby(["Gender"]).sum()["Price"].rename("Total Purchase Value")
gender_purchase_average = purchase_data.groupby(["Gender"]).mean()["Price"].rename("Average Purchase Price")
gender_purchase_count = purchase_data.groupby(["Gender"]).count()["Price"].rename("Purchase Count")

purchase_total_per_gender = gender_purchase_total/gender_demographics["Total Count"]

#Display the summary data frame

purchase_analysis = pd.DataFrame({ "Purchase Count" : gender_purchase_count,
                                "Total Purchase Value" : gender_purchase_total,
                                "Average Purchase Price" : gender_purchase_average,
                                "Avg.Purchase Total per Person" : purchase_total_per_gender})
purchase_analysis["Avg.Purchase Total per Person"] = purchase_analysis["Avg.Purchase Total per Person"].map("${:,.2f}".format)
purchase_analysis["Average Purchase Price"] = purchase_analysis["Average Purchase Price"].map("${:,.2f}".format)
purchase_analysis["Total Purchase Value"] = purchase_analysis["Total Purchase Value"].map("${:,.2f}".format)
purchase_analysis["Purchase Count"] = purchase_analysis["Purchase Count"].map("{:,}".format)

purchase_analysis


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[6]:


#Establish bins

age_bins = [0,9.90,14.90,19.90,24.90,29.90,34.90,39.90,999]
group_names = ["<10","10-14","15-19","20-24","25-29","30-34","34-39","40+"]
player_demographics["Age Ranges"] = pd.cut(player_demographics["Age"], age_bins, labels=group_names)

age_demographics_totals = player_demographics["Age Ranges"].value_counts()
age_demographics_percents = age_demographics_totals / num_players
age_demographics = pd.DataFrame({"Total Count": age_demographics_totals,
                                 "Percentage of Players": age_demographics_percents})

age_demographics["Percentage of Players"] = age_demographics["Percentage of Players"].map("{:,.2%}".format)

#Display the summary data frame

age_demographics = age_demographics.sort_index()
age_demographics


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[10]:


#Establish ranges by age

purchase_data["Age Ranges"] = pd.cut(player_demographics["Age"], age_bins, labels=group_names)

#calculations

age_purchase_total = purchase_data.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")
avg_purchase_price = purchase_data.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")
age_count = purchase_data.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

normalized_total = age_purchase_total/age_demographics["Total Count"]

age_data = pd.DataFrame({
                        "Purchase Count": age_count,
                        "Average Purchase Price": avg_purchase_price,
                        "Total Purchase Value": age_purchase_total,
                        "Average Total Purchase per person": normalized_total 
                        })

#Display the summary data frame

age_data["Average Purchase Price"] = age_data["Average Purchase Price"].map("${:,.2f}".format)
age_data["Total Purchase Value"] = age_data["Total Purchase Value"].map("${:,.2f}".format)
age_data["Average Total Purchase per person"] = age_data["Average Total Purchase per person"].map("{:,.2f}".format)


age_data = age_data.sort_index()

age_data


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[8]:


user_total = purchase_data.groupby(["SN"]).sum()["Price"].rename("Total Purchase Value")
user_average = purchase_data.groupby(["SN"]).mean()["Price"].rename("Average Purchase Value")
user_count = purchase_data.groupby(["SN"]).count()["Price"].rename("Purchase Count")

user_data = pd.DataFrame({
                        "Total Purchase Value" : user_total,
                        "Average Purchase Value" : user_average,
                        "Purchase Count" : user_count
                        })
user_sorted = user_data.sort_values("Total Purchase Value", ascending=False)

user_sorted["Total Purchase Value"] = user_sorted["Total Purchase Value"].map("${:,.2f}".format)
user_sorted["Average Purchase Value"] = user_sorted["Average Purchase Value"].map("${:,.2f}".format)

user_sorted


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, average item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[13]:


item_data = purchase_data[["Item ID", "Item Name", "Price"]]

#Perform Calculations

#item_data.groupby(["Item ID", "Item Name"]).sum(["Price"]).rename(columns={"Price":"Total Purchase Price"})
total_item_purchase = item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Price")
average_item_purchase = item_data.groupby(["Item ID", "Item Name"]).mean()["Price"].rename("Average Purchase Price")
item_count = item_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")

# #create df
item_data = pd.DataFrame({
                        "Total Purchase Value" : total_item_purchase,
                        "Average Purchase Value" : average_item_purchase,
                        "Purchase Count" : item_count })

#sort values

item_data_sorted = item_data.sort_values("Purchase Count", ascending=False)


item_data_sorted["Total Purchase Value"] = item_data_sorted["Total Purchase Value"].map("${:,.2f}".format)
item_data_sorted["Average Purchase Value"] = item_data_sorted["Average Purchase Value"].map("${:,.2f}".format)

item_data_sorted


# In[ ]:





# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[17]:


item_data_sorted = item_data.sort_values("Total Purchase Value", ascending=False)

item_data_sorted["Total Purchase Value"] = item_data_sorted["Total Purchase Value"].map("${:,.2f}".format)
item_data_sorted["Average Purchase Value"] = item_data_sorted["Average Purchase Value"].map("${:,.2f}".format)

item_data_sorted


# In[ ]:





# In[ ]:





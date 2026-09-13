import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load CSV without assuming header row
raw_df = pd.read_csv("Amazon Sale Report.csv", header=None, low_memory=False)

# Find the row containing "Order ID"
header_row = raw_df.apply(
    lambda row: row.astype(str).str.strip().eq("Order ID").any(),
    axis=1
).idxmax()

print("Header row found at:", header_row)

# Set correct header
df = pd.read_csv(
    "Amazon Sale Report.csv",
    header=header_row,
    low_memory=False
)

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Remove duplicate header rows
df = df[df["Order ID"].astype(str).str.strip() != "Order ID"].copy()

# Remove unnecessary columns
df = df.drop(columns=["Unnamed: 22"], errors="ignore")

# Convert Date
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m-%d-%y",
    errors="coerce"
)

# Convert numeric columns
df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

print(df.head())
print(df.columns)
print(df.shape)
print(df.info())
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

print(df["Status"].value_counts())

total_orders =df['Order ID'].nunique()
total_quantity =df["Qty"].sum()
total_sales = df["Amount"].sum()

average_order_value = total_sales/total_orders

cancelled_orders =(df["Status"] == "Cancelled").sum()
cancellation_rate =(cancelled_orders/len(df))*100

print(f"Total orders = {total_orders}")
print(f"Total Quantity= {total_quantity}")
print(f"Total Sales = {total_sales}")
print(f" Average order value= {average_order_value}")
print(f"Cancelled orders = {cancelled_orders}")
print(f"Cancellation Rate = {cancellation_rate}")

# Order Status


plt.figure(figsize=(10, 7))

status_count = df["Status"].value_counts().sort_values()

plt.barh(status_count.index, status_count.values)

plt.title("Order Status Distribution", fontsize=16)
plt.xlabel("Number of Orders", fontsize=12)
plt.ylabel("Order Status", fontsize=12)

plt.tight_layout()
plt.show()

# Category Analysis

category_sales = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
print(category_sales)

plt.figure(figsize=(10,5))
category_sales.plot(kind='bar',color='green')
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("sales")
plt.tight_layout()
plt.grid(axis='y')
plt.xticks(rotation=0)
plt.show()

# Size Analysis


size_sales = df.groupby("Size")["Amount"].sum().sort_values(ascending=False)
print(size_sales)

plt.figure(figsize=(10,5))
size_sales.plot(kind="bar")
plt.title("Sales by size")
plt.xlabel("Size")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.show()

# State Wise Analysis


state_sales = (df.groupby('ship-state')["Amount"].sum().sort_values(ascending=False))
print(state_sales)

plt.figure(figsize=(10,6))
state_sales.head(10).plot(kind="pie",autopct="%1.1f%%")
plt.title(" Top 10 States by sales")
plt.show()

# Monthly Sales Trend 


df["Month"] = df["Date"].dt.to_period("M")
monthly_sales = df.groupby("Month")["Amount"].sum()
print(monthly_sales)

plt.figure(figsize=(10,5))
monthly_sales.plot(kind="line",marker="D",color='red',markersize=10)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(axis='y')
plt.show()

# Fulfilment Analysis

fulfilment_orders=df["Fulfilment"].value_counts()
print(fulfilment_orders)

plt.figure(figsize=(7,5))
ax=fulfilment_orders.plot(kind='bar')
plt.bar_label(ax.containers[0])
plt.title("Orders by Fulfilment type")
plt.xlabel("Fulfilment")
plt.ylabel("Number of orders")
plt.xticks(rotation=0)
plt.show()

# Top 10 products / Styles 


top_styles = (df.groupby("Style")["Amount"].sum().sort_values(ascending=False).head(10))
print(top_styles)

plt.figure(figsize=(10,6))
top_styles.plot(kind='bar',color='purple')
plt.title(" Top 10 Styles by Sales")
plt.xlabel("Style")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.show()


# B2B vs B2C 

b2b_sales = df.groupby("B2B")["Amount"].sum()
print(" B2B vs B2C Sales")
print(b2b_sales)

plt.figure(figsize=(7,5))

ax= b2b_sales.plot(kind='bar',color=['skyblue','orange'])

plt.title("B2B Vs B2C Sales")
plt.xlabel("Customer Type")
plt.ylabel("Sales")
plt.xticks([0,1],['B2C',"B2B"],rotation=0)
plt.bar_label(ax.containers[0],fmt="%.0f")
plt.show()


# Revemue vs Quantity by Category 

category_analysis = (
    df.groupby("Category")
    .agg(
        Total_Sales=("Amount", "sum"),
        Total_Quantity=("Qty", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
)

print("Category Revenue Vs Quantity")
print(category_analysis)


fig, ax1 = plt.subplots(figsize=(10, 6))

x = np.arange(len(category_analysis))

# Sales bar
ax1.bar(
    x - 0.2,
    category_analysis["Total_Sales"],
    width=0.4,
    color="green",
    label="Sales"
)

ax1.set_xlabel("Category")
ax1.set_ylabel("Sales", color="green")

# Quantity bar
ax2 = ax1.twinx()

ax2.bar(
    x + 0.2,
    category_analysis["Total_Quantity"],
    width=0.4,
    color="orange",
    label="Quantity"
)

ax2.set_ylabel("Quantity", color="orange")

ax1.set_xticks(x)
ax1.set_xticklabels(category_analysis.index)

plt.title("Category-wise Sales vs Quantity")

plt.tight_layout()
plt.show()



# from sqlalchemy import create_engine
# username= "postgres"
# password= "Vipul#9453"
# host = "localhost"
# port = "5432"
# database= "Amazon Sales Analysis"

# engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# table_name = "amazon_sales"
# df.to_sql(table_name,engine,if_exists="replace",index=False)

# print(f"Data successfully loaded into table '{table_name}'in database '{database}'.")


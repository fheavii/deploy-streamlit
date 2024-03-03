import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

Bike_data = pd.read_csv("Bike_data.csv")

datetime_columns = ["dteday"]
Bike_data.sort_values(by="dteday", inplace=True)
Bike_data.reset_index(inplace=True)
for column in datetime_columns:
    Bike_data[column] = pd.to_datetime(Bike_data[column])

datetime_columns = ["dteday"]
Bike_data.sort_values(by="dteday", inplace=True)
Bike_data.reset_index(inplace=True)
for column in datetime_columns:
    Bike_data[column] = pd.to_datetime(Bike_data[column])

min_date = Bike_data["dteday"].min()
max_date = Bike_data["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/fheavii/SUBMISSION/main/bike%20sharing%20(1).png")
    min_date = Bike_data["dteday"].min()
    max_date = Bike_data["dteday"].max()
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_data = Bike_data[(Bike_data["dteday"] >= str(start_date)) & (Bike_data["dteday"] <= str(end_date))]

selected_seasons = st.sidebar.multiselect(
    label="Season",
    options=Bike_data["season_label"].unique(),  
    default=Bike_data["season_label"].unique() 
) 

filtered_data = Bike_data[Bike_data["season_label"].isin(selected_seasons)]

selected_workingday = st.sidebar.radio(
    label="Select Working Days or Not",
    options=["Working Day", "Non-Working Day", "Semua"], 
    index=2  
)

if selected_workingday == "Working Day":
    filtered_data = Bike_data[Bike_data["workingday_hour"] == 1]
elif selected_workingday == "Non-Working Day":
    filtered_data = Bike_data[Bike_data["workingday_hour"] == 0]

avg_season = filtered_data.groupby('season_label')['cnt_day'].mean().reset_index().sort_values("cnt_day")

avg_season = filtered_data.groupby('season_label')['cnt_day'].mean().reset_index().sort_values("cnt_day")

avg_hourly_rentals = filtered_data.groupby(['hr', 'workingday_hour'])['cnt_hour'].mean().reset_index().sort_values("hr")
working_day_data = avg_hourly_rentals[avg_hourly_rentals['workingday_hour'] == 1]
non_working_day_data = avg_hourly_rentals[avg_hourly_rentals['workingday_hour'] == 0]

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Rentals')
col1, col2 = st.columns(2)
with col1:
    total_rentals = filtered_data['cnt_day'].sum()  
    st.metric("Total Rentals", value=total_rentals)
with col2:
    total_days = filtered_data['dteday'].nunique()
    st.metric("Total Days", value=total_days)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(filtered_data["dteday"], filtered_data["cnt_day"], marker='o', linewidth=2, color="darkgreen")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Rentals by Season")
fig_season = plt.figure(figsize=(10, 6)) 
sns.barplot(x='cnt_day', y='season_label', data=avg_season, palette='summer') 
plt.xlabel("Average Rentals", fontsize=12)
plt.ylabel("Season", fontsize=12)
plt.title("Average Bike Sharing by Season", fontsize=15)
plt.xticks(rotation=45)  
plt.legend() 
plt.grid(False)
st.pyplot(fig_season) 

st.subheader("Rentals by Working Day and Non-Working Day")
fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(working_day_data['hr'], working_day_data['cnt_hour'], label='Working Day', marker='o', color='darkgreen')
plt.plot(non_working_day_data['hr'], non_working_day_data['cnt_hour'], label='Non-Working Day', marker='o', color='limegreen')
plt.xlabel("Hour", fontsize=12)
plt.ylabel("Average Rentals", fontsize=12)
plt.title("Average Hourly Bike Rentals by Working Day and Non-Working Day", fontsize=15)
plt.xticks(range(24))
plt.legend()
plt.grid(True)
st.pyplot(fig)
import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
df = pd.read_csv("dataset/hotel_bookings_cleaned.csv")
tourism_df = pd.read_csv("dataset/india_tourism_data.csv")

# Convert date column
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

# --- Streamlit App ---
st.set_page_config(page_title="Hotel Booking & Tourism Dashboard", layout="wide")
st.title("🏨 Hotel Booking & Tourism Trend Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("📌 Hotel Booking Filters")
hotel_type = st.sidebar.multiselect("Select Hotel Type:", options=df['hotel'].unique(), default=df['hotel'].unique())
year_filter = st.sidebar.slider("Select Year:", min_value=int(df['reservation_status_date'].dt.year.min()),
                                 max_value=int(df['reservation_status_date'].dt.year.max()), value=(2015, 2017))

st.sidebar.markdown("---")
st.sidebar.header("🌏 Tourism Filters")
states = st.sidebar.multiselect("Select States:", options=tourism_df['State'].unique(), default=tourism_df['State'].unique())
year_range = st.sidebar.slider("Select Year Range:", int(tourism_df['Year'].min()), int(tourism_df['Year'].max()), (2015, 2020))

tourist_type = st.sidebar.radio("Tourist Type", ["Both", "Domestic", "Foreign"])

# --- Filter Hotel Data ---
filtered_df = df[
    (df['hotel'].isin(hotel_type)) &
    (df['reservation_status_date'].dt.year >= year_filter[0]) &
    (df['reservation_status_date'].dt.year <= year_filter[1])
]

# --- Filter Tourism Data ---
tourism_filtered = tourism_df[
    (tourism_df['State'].isin(states)) &
    (tourism_df['Year'] >= year_range[0]) &
    (tourism_df['Year'] <= year_range[1])
]

# --- KPIs ---
total_bookings = len(filtered_df)
cancellations = filtered_df['is_canceled'].sum()
avg_adr = round(filtered_df['adr'].mean(), 2)

col1, col2, col3 = st.columns(3)
col1.metric("📊 Total Bookings", f"{total_bookings}")
col2.metric("❌ Cancellations", f"{cancellations}")
col3.metric("💰 Avg. ADR", f"{avg_adr} €")

st.markdown("---")

# --- Hotel Booking Visualizations ---
st.subheader("📅 Monthly Bookings")
monthly = filtered_df['arrival_date_month'].value_counts().reindex([
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
])
fig1 = px.bar(x=monthly.index, y=monthly.values, labels={'x': 'Month', 'y': 'Bookings'}, title="Monthly Bookings")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🌍 Top 10 Countries")
top_countries = filtered_df['country'].value_counts().head(10)
fig2 = px.bar(x=top_countries.values, y=top_countries.index, orientation='h', title="Top 10 Booking Countries",
              labels={'x': 'Bookings', 'y': 'Country'})
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📈 Average Daily Rate (ADR) by Month")
filtered_df['month'] = pd.Categorical(filtered_df['arrival_date_month'], categories=[
    'January','February','March','April','May','June','July',
    'August','September','October','November','December'], ordered=True)
monthly_adr = filtered_df.groupby('month')['adr'].mean().reset_index()
fig3 = px.line(monthly_adr, x='month', y='adr', markers=True, title="ADR per Month")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📊 Top 10 Booking Agents")
agent_counts = filtered_df['agent'].value_counts().head(10)
fig4 = px.bar(x=agent_counts.index.astype(str), y=agent_counts.values,
              labels={'x': 'Agent ID', 'y': 'Bookings'}, title="Top 10 Booking Agents")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("🚪 Reserved Room Types")
room_counts = filtered_df['reserved_room_type'].value_counts()
fig5 = px.pie(values=room_counts.values, names=room_counts.index, title="Reserved Room Type Distribution")
st.plotly_chart(fig5, use_container_width=True)

st.subheader("📅 Bookings Over Time")
filtered_df['Year'] = filtered_df['reservation_status_date'].dt.year
yearly_bookings = filtered_df.groupby('Year').size().reset_index(name='Bookings')
fig6 = px.bar(yearly_bookings, x='Year', y='Bookings', title="Yearly Bookings")
st.plotly_chart(fig6, use_container_width=True)

# --- Tourism Visualizations ---
st.subheader("📉 Tourist Arrivals Over Time")

if tourist_type == "Domestic":
    agg_tourism = tourism_filtered.groupby('Year')[['Domestic_Tourists']].sum().reset_index()
    fig7 = px.line(agg_tourism, x='Year', y='Domestic_Tourists', markers=True)
elif tourist_type == "Foreign":
    agg_tourism = tourism_filtered.groupby('Year')[['Foreign_Tourists']].sum().reset_index()
    fig7 = px.line(agg_tourism, x='Year', y='Foreign_Tourists', markers=True)
else:
    agg_tourism = tourism_filtered.groupby('Year')[['Foreign_Tourists', 'Domestic_Tourists']].sum().reset_index()
    fig7 = px.line(agg_tourism, x='Year', y=['Foreign_Tourists', 'Domestic_Tourists'], markers=True)

fig7.update_layout(title="Tourist Arrivals Over Time", xaxis_title="Year", yaxis_title="Number of Tourists")
st.plotly_chart(fig7, use_container_width=True)

st.subheader("🏞️ Top 10 States by Tourist Count")
top_states = tourism_filtered.groupby('State')[['Foreign_Tourists', 'Domestic_Tourists']].sum()
top_states['Total'] = top_states['Foreign_Tourists'] + top_states['Domestic_Tourists']
top_10_states = top_states.sort_values(by='Total', ascending=False).head(10).reset_index()
fig8 = px.bar(top_10_states, x='Total', y='State', orientation='h',
              title="Top 10 States by Total Tourist Count", color='Total')
st.plotly_chart(fig8, use_container_width=True)

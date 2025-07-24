import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def trend_analysis():
    df = pd.read_csv('dataset/hotel_bookings_cleaned.csv')
    os.makedirs("outputs", exist_ok=True)

    # Lead Time vs Cancellation
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='is_canceled', y='lead_time', data=df)
    plt.title("Lead Time vs. Cancellation")
    plt.xticks([0, 1], ['Not Canceled', 'Canceled'])
    plt.ylabel("Lead Time (days)")
    plt.savefig("outputs/lead_time_vs_cancellation.png")
    print("[✔] Saved 'outputs/lead_time_vs_cancellation.png'")

    # Top 10 countries
    top_countries = df['country'].value_counts().head(10)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="cubehelix")
    plt.title("Top 10 Booking Countries")
    plt.xlabel("Number of Bookings")
    plt.ylabel("Country")
    plt.savefig("outputs/top_countries.png")
    print("[✔] Saved 'outputs/top_countries.png'")

    # ADR by month
    df['month'] = pd.Categorical(df['arrival_date_month'], categories=[
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ], ordered=True)

    monthly_adr = df.groupby('month')['adr'].mean()

    plt.figure(figsize=(10,5))
    monthly_adr.plot(marker='o')
    plt.title("Average Daily Rate (ADR) per Month")
    plt.ylabel("ADR (₹)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.savefig("outputs/monthly_adr.png")
    print("[✔] Saved 'outputs/monthly_adr.png'")

if __name__ == "__main__":
    trend_analysis()

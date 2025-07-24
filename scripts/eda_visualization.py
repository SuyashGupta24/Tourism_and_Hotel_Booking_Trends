import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def eda():
    df = pd.read_csv('dataset/hotel_bookings_cleaned.csv')
    
    os.makedirs("outputs", exist_ok=True)

    # Monthly Bookings
    monthly = df['arrival_date_month'].value_counts().reindex([
        'January','February','March','April','May','June',
        'July','August','September','October','November','December'
    ])

    plt.figure(figsize=(10,5))
    ax = sns.barplot(x=monthly.index, y=monthly.values, palette='viridis')
    plt.title("Monthly Bookings")
    plt.xticks(rotation=45)
    for i, val in enumerate(monthly.values):
        ax.text(i, val + 100, str(val), ha='center')
    plt.tight_layout()
    plt.savefig("outputs/monthly_bookings.png")
    print("[✔] Saved 'outputs/monthly_bookings.png'")

    # Cancellation Pie Chart
    cancel_rate = df['is_canceled'].value_counts(normalize=True)
    labels = ['Not Canceled', 'Canceled']
    plt.figure()
    plt.pie(cancel_rate, labels=labels, autopct='%1.1f%%', colors=['skyblue', 'orange'])
    plt.title("Booking Cancellation Rate")
    plt.savefig("outputs/cancellation_rate.png")
    print("[✔] Saved 'outputs/cancellation_rate.png'")

if __name__ == "__main__":
    eda()

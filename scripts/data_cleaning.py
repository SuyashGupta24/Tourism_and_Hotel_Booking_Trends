import pandas as pd
import os

def clean_data():
    file_path = 'dataset/hotel_bookings.csv'
    
    if not os.path.exists(file_path):
        print("[✖] File not found:", file_path)
        return

    df = pd.read_csv(file_path)

    # Drop unnecessary columns
    df.drop(['agent', 'company'], axis=1, inplace=True)

    # Fill missing values
    df['children'].fillna(0, inplace=True)
    df['country'].fillna(df['country'].mode()[0], inplace=True)

    # Convert date columns
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')

    # Save cleaned data
    cleaned_path = 'dataset/hotel_bookings_cleaned.csv'
    df.to_csv(cleaned_path, index=False)
    print(f"[✔] Data cleaned and saved at '{cleaned_path}'")

if __name__ == "__main__":
    clean_data()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def tourism_analysis():
    df = pd.read_csv("dataset/india_tourism_data.csv")
    os.makedirs("outputs", exist_ok=True)
    # Convert year column to int (if not already)
    df['Year'] = df['Year'].astype(int)

    # Total tourists per year (Indian + Foreign)
    df['Total Tourists'] = df['Domestic_Tourists'] + df['Foreign_Tourists']

    # Plot yearly tourism trend
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='Year', y='Total Tourists', data=df, marker='o')
    plt.title("Total Tourism in India Over Years")
    plt.xlabel("Year")
    plt.ylabel("Number of Tourists")
    plt.grid(True)
    plt.savefig("outputs/tourism_total_trend.png")
    print("[✔] Saved 'tourism_total_trend.png'")

    # Top 5 states in latest year
    latest_year = df['Year'].max()
    latest_df = df[df['Year'] == latest_year].sort_values(by='Total Tourists', ascending=False).head(5)

    plt.figure(figsize=(8, 5))
    sns.barplot(x='Total Tourists', y='State', data=latest_df, palette='coolwarm')
    plt.title(f"Top 5 Tourist States in {latest_year}")
    plt.savefig("outputs/top_states_tourism.png")
    print(f"[✔] Saved 'top_states_tourism.png'")

if __name__ == "__main__":
    tourism_analysis()

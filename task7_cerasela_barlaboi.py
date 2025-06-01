import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '**********',
    database = 'movies_db'
)

if(conn == None):
    print("There is no connection to database.")
else:
    print('Connection is created.')
    
cursor = conn.cursor()

print("Connection established successfully, and the cursor has been created.")

query = """
SELECT genre, budget, box_office
FROM movies
WHERE budget IS NOT NULL AND box_office IS NOT NULL
"""
movies = pd.read_sql_query(query, conn)

average_data = movies.groupby('genre')[['budget', 'box_office']].mean()

average_sorted = average_data.sort_values('box_office', ascending=False)

top_profitable = average_sorted.head(3)

top_unprofitable = average_sorted.tail(3)

top_profitable[['budget', 'box_office']] /= 1_000_000
top_unprofitable[['budget', 'box_office']] /= 1_000_000

def plot_genres(data, title):
    plt.figure(figsize=(8, 5))
    bar_width = 0.4
    x = range(len(data))

    plt.bar(x, data['budget'], width=bar_width, label='Buget Mediu', color='cornflowerblue')
    plt.bar([i + bar_width for i in x], data['box_office'], width=bar_width, label='Câștig Mediu', color='mediumseagreen')

    plt.xlabel("Genul Filmului", fontsize=12)
    plt.ylabel("Sume Medii (Mil. USD)", fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xticks([i + bar_width / 2 for i in x], data.index, rotation=45, ha='right')

    for i, (b, r) in enumerate(zip(data['budget'], data['box_office'])):
        plt.text(i, b + 0.5, f'{b:.1f}M', ha='center', va='bottom', fontsize=8)
        plt.text(i + bar_width, r + 0.5, f'{r:.1f}M', ha='center', va='bottom', fontsize=8)

    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

plot_genres(top_profitable, "Top 3 Genuri Cele Mai Profitabile")

plot_genres(top_unprofitable, "Top 3 Genuri Cele Mai Puțin Profitabile")


correlation = movies[['budget', 'box_office']].corr().iloc[0, 1]

print(f"Corelația Pearson între buget și câștig: {correlation:.2f}")

query_countries = """
SELECT country, AVG(box_office) AS avg_revenue
FROM movies
WHERE box_office IS NOT NULL AND country IS NOT NULL
GROUP BY country
ORDER BY avg_revenue DESC
LIMIT 5
"""
top_countries = pd.read_sql_query(query_countries, conn)
top_countries['avg_revenue'] /= 1_000_000  # milioane USD

import seaborn as sns
plt.figure(figsize=(10, 6))
sns.barplot(data=top_countries, x='country', y='avg_revenue', palette='viridis')

plt.title('Top 5 țări după câștig mediu al filmelor (în milioane USD)', fontsize=14, fontweight='bold')
plt.xlabel('Țara producătoare', fontsize=12)
plt.ylabel('Câștig Mediu (Mil. USD)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

query_top_movies = """
SELECT title, box_office
FROM movies
WHERE box_office IS NOT NULL
ORDER BY box_office DESC
LIMIT 10
"""

top_movies = pd.read_sql_query(query_top_movies, conn)

print("Top 10 filme după câștiguri:")
print(top_movies)

correlation = movies[['budget', 'box_office']].corr().iloc[0, 1]
print(f"Corelaţia Pearson între buget şi câştig: {correlation:.2f}")

cursor.close()
conn.close()

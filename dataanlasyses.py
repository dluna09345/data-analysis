from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define your database connection parameters
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_NAME = 'data-analysis'

# Build the connection string
database_url = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# Create the engine
engine = create_engine(database_url)

# Load data into a DataFrame
query = 'SELECT * FROM nba_team_stats'
df = pd.read_sql(query, engine)

def average_three_pt_percentage_overall(df):
    season_avg = df.groupby(['TEAM', 'Season'])['3P%'].mean().reset_index()
    team_overall_avg = season_avg.groupby('TEAM')['3P%'].mean().reset_index()
    team_overall_avg = team_overall_avg.sort_values(by='3P%', ascending=False)   
    return team_overall_avg
avg_df = average_three_pt_percentage_overall(df)
def plot_scatter_avg_three_pt_percentage_overall(avg_df):
    plt.figure(figsize=(10, 6))
    plt.scatter(avg_df['TEAM'], avg_df['3P%'], color='orange', s=100)
    plt.title('Overall Average Three-Point Percentage by Team')
    plt.xlabel('Team')
    plt.ylabel('Average Three-Point Percentage')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('graphs/overall_avg_three_pt_percentage.png')
    plt.show()

def rank_teams_by_total_points(df):
    grouped = df.groupby('TEAM')['PTS'].sum().reset_index()
    ranked = grouped.sort_values(by='PTS', ascending=False)
    return ranked
total_points_df = rank_teams_by_total_points(df)
def plot_total_points_bar(total_points_df):
    plt.figure(figsize=(10, 6))
    plt.bar(total_points_df['TEAM'], total_points_df['PTS'], color='teal')
    plt.title('Total Points by Team')
    plt.xlabel('Team')
    plt.ylabel('Total Points (PTS)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('graphs/total_points_bar.png')
    plt.show()

def total_three_pointers_made(df):
    grouped = df.groupby('TEAM')['3PM'].sum().reset_index()
    grouped = grouped.sort_values(by='3PM', ascending=False)
    return grouped
total_3pm_df = total_three_pointers_made(df)
def plot_total_three_pointers_bar(total_3pm_df):
    plt.figure(figsize=(10, 6))
    plt.barh(total_3pm_df['TEAM'], total_3pm_df['3PM'], color='salmon')
    plt.title('Total Three-Pointers Made by Team')
    plt.xlabel('Total Three-Pointers Made')
    plt.ylabel('Team')
    plt.tight_layout()
    plt.savefig('graphs/total_three_pointers_bar.png')
    plt.show()

def top_improved_teams(df):
    grouped = df.groupby(['TEAM', 'Season'])['3P%'].mean().reset_index()
    grouped = grouped.sort_values(by=['TEAM', 'Season'])
    pivot = grouped.pivot(index='TEAM', columns='Season', values='3P%')
    pivot['Improvement'] = pivot.iloc[:, -1] - pivot.iloc[:, 0]
    pivot = pivot.reset_index()
    top_improved = pivot.sort_values(by='Improvement', ascending=False)  
    return top_improved[['TEAM', 'Improvement']]
top_improved_df = top_improved_teams(df)
#seaborn scatterplot for improvement
def plot_improvement_scatter(top_improved_df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=top_improved_df, x='TEAM', y='Improvement', color='green', s=100)
    plt.title('Teams Ranked by 3P% Improvement')
    plt.xlabel('Team')
    plt.ylabel('Improvement in 3P%')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('graphs/improvement_scatter.png')
    plt.show()

result = average_three_pt_percentage_overall(df)
print("Top 5 teams by average three-point percentage:")
print(result.head(5))
plot_scatter_avg_three_pt_percentage_overall(avg_df)

result = rank_teams_by_total_points(df)
print("Top 5 teams by total points scored:")
print(result.head(5))
plot_total_points_bar(total_points_df)

result = total_three_pointers_made(df)
print("Total three-pointers made by each team:")
print(result.head(5))
plot_total_three_pointers_bar(total_3pm_df)

result = top_improved_teams(df)
print("Top 5 teams with the most improvement in three-point percentage:")
print(result.head(5))
plot_improvement_scatter(top_improved_df)

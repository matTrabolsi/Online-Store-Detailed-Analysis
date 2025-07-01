import pandas as pd
import pyodbc 
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

#connecting to database and fetching the reviews table as data frame
def fetch_data_from_sql():
    conn_str = (
        "Driver={SQL Server};"  # Specify the driver for SQL Server
        "Server=DESKTOP-BA94EQH\SQLEXPRESS;"  # Specify your SQL Server instance
        "Database=PortfolioProject_MarketingAnalytics;"  # Specify the database name
        "Trusted_Connection=yes;"  # Use Windows Authentication for the connection
    )

    conn = pyodbc.connect(conn_str)
    query = "SELECT ReviewID, CustomerID, ProductID, Rating, ReviewText FROM customer_reviews"

    df = pd.read_sql(query, conn)

    conn.close()

    return df

customer_reviews_df = fetch_data_from_sql()

sia = SentimentIntensityAnalyzer()

# return a score from -1 'bad' to +1 'good'
def calculte_sentimnet(review):
    sentiment = sia.polarity_scores(review)
    
    return sentiment['compound']

# categorize the reviews based on score and rating
def categorize_sentiment(score, rating):
    if score > 0.05:
        if rating >= 4:
            return 'Positive'
        elif rating == 3:
            return 'Mixed Positive'
        else:
            return 'Mixed Negative'
        
    elif score < -0.05:
        if rating <=2:
            return 'Negative'
        elif rating == 3:
            return 'Mixed Negative'
        else:
            return'Mixed Positive'
    
    else:
        if rating >= 4:
            return 'Positive'
        elif rating <= 2:
            return 'Negative'
        else:
            return 'Neutral'

#bucket sentiment scores into text ranges
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'  # Strongly positive 
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'  # Mildly positive 
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Mildly negative 
    else:
        return '-1.0 to -0.5'  # Strongly negative 

customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculte_sentimnet)

customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)# using lambda to make short function, using axis=1 to select row

customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

print(customer_reviews_df.head())

#(index=false) rmove pandas default extra indexing 
customer_reviews_df.to_csv('fact_customer_reviews_with_sentiment.csv', index=False) 
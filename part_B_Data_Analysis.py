import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Q1
# apps:
def get_file(file_name):
    data_file = None
    try:
        data_file = pd.read_csv(file_name)
    except:
        print("ERROR reading files")
    finally:
        return data_file

apps_data = get_file("apps.csv")

# Q2.1
print('--------apps--------')
print('Number of rows: ' + str(apps_data.shape[0]) +
      '\n' + 'Number of cols:  ' + str(apps_data.shape[1]))

# Q2.2
print(apps_data.columns)
print('-------user_reviews-------')
reviews_data = get_file('user_reviews.csv')
print('Number of rows: ' + str(reviews_data.shape[0]) +
      '\n' + 'Number of cols:  ' + str(reviews_data.shape[1]))
print(reviews_data.columns)

# Q 2 - First Exploring:
print('----number of Categories---')
apps_categories_count = apps_data['Category'].drop_duplicates().count()
print("Total count of apps categories: {}".format(apps_categories_count))



# print('--Q 2.2-The Heaviest app---')
apps_data['Size'] = apps_data['Size'].replace(to_replace='Varies with device', value=None, regex=True)
apps_data['Size'] = apps_data['Size'].replace({'[kK]': '*1e3', '[mM]': '*1e6'}, regex=True).map(pd.eval).astype(int)
heaviest_app = apps_data[apps_data['Size'] == apps_data['Size'].max()][['App','Size']].drop_duplicates()
print("\nThe heaviest app:\n {}".format(heaviest_app))

print('--Q 2.3 -The app with the most installs---')
most_install = apps_data[apps_data['Installs'].str.replace('+','').str.replace(',','').astype(int)==
                         apps_data['Installs'].str.replace('+','').str.replace(',','').astype(int).max()][['App','Installs']].drop_duplicates()
print("The app with the most installs is:\n {}".format(most_install))


print('--Q 2.4 -The most updated App---')
apps_data['Last Updated'] = pd.to_datetime(apps_data['Last Updated'])
print("The most updated date is: " , apps_data['Last Updated'].max())
print(apps_data[apps_data['Last Updated'] == apps_data['Last Updated'].max()]['App'])


print('--Q 2.5 -The most popular app genre---')
genres = apps_data['Genres'].value_counts().head(1)
print("The most popular app genre:\n {}".format(genres))


# Q3 Analysis:
print('-- Q3.1 -Number of Apps fof each genre---')
num = apps_data['Genres'].value_counts()
print(num)

print('-- Q3.2 -list of the free apps---')
list_of_free_App = apps_data[apps_data['Type'] == 'Free']['App'].drop_duplicates()
print('the list of the Free Apps is: {}'.format(list_of_free_App))

print('--Q3.3-The pop Genres---')   # good
apps_data['Installs'] = apps_data['Installs'].apply(lambda x: x.replace('+', '')).apply(lambda x: x.replace(',', '')).astype(int)
most_pop = apps_data.groupby('Type')['Installs'].sum().sort_values().tail(1)
print(most_pop)


# Q3.4
print('Q3.4')
def get_app_details_by_letter(letter):
    letter = str(letter)
    return (apps_data[apps_data['App'].str.startswith(letter, na=False)]['App'])

# Q4 Advanced Analysis
print('--Q 4.1 -The apps classified as Positive sentiment---') # good
pos = reviews_data[reviews_data['Sentiment'] == 'Positive']['App'].drop_duplicates().count()
print(pos)

print('--Q 4.2.1 -The apps classified as Neutral sentiment---') # good
neu = reviews_data[reviews_data['Sentiment'] == 'Neutral']['App'].drop_duplicates().count()
print(neu)

print('--Q 4.2.2 -The apps classified as Negative sentiment---') #good
neg = reviews_data[reviews_data['Sentiment'] == 'Negative']['App'].drop_duplicates().count()
print(neg)


print('--Q 4.3 -What is the sentiment of the app with the most rating?')
full_d = pd.merge(apps_data, reviews_data, on='App')
full_A = pd.merge(reviews_data, apps_data, on='App', how='left')
most_rating_A = full_A[full_A['Rating'] == full_A['Rating'].max()][['App', 'Sentiment']].drop_duplicates()
max_A = full_A['Rating'].max()
print("B - The sentiment of the apps with the most rating:\n {}".format(most_rating_A))



print('--Q 4.4 -The average polarity of free apps')
average_polarity = full_d[full_d['Type'] == 'Free']['Sentiment_Polarity'].mean()
print("\nThe average polarity of free apps:\n {}".format(average_polarity))


print('--Q 4.5 - get_average_polarity---')
def get_average_polarity(app_name):
    app_name = str(app_name)
    if app_name not in reviews_data[reviews_data['App'] == app_name]['App'].to_list():
        return app_name + " does not exist in the database"
    else:
        reviews_data['Sentiment_Polarity'] = reviews_data['Sentiment_Polarity'].replace('nan','0')
        average_polarity = reviews_data[reviews_data['App'] == app_name]['Sentiment_Polarity'].mean()
        return average_polarity


print('--Q 4.6 - most app review---')
def get_sentiment(app_name):
    if app_name not in reviews_data[reviews_data['App'] == app_name]['App'].to_list():
        return app_name + " does not exist in the database"
    else:
        all_sentiment = get_average_polarity(app_name)
        if all_sentiment > 0:
            return "Positive"
        elif all_sentiment < 0:
            return "Negetive"
        else:
            return "Neutral"


# ------ Q5 - Advanced Analysis + Visualization  ------
# 1
reviews_data['Sentiment'].value_counts().plot(kind='bar', color=['navy','royalblue','cornflowerblue'], rot=0)
plt.xlabel('Sentiment')
plt.ylabel('amount')
plt.title('sentiment ranks')
plt.show()

# 2
apps_data.groupby('Genres')['Rating'].mean().plot(kind='bar', color='royalblue',fontsize=4, figsize=(17, 17))
plt.xlabel('Genre')
plt.ylabel('Average')
plt.title('Average Rating by Genre')
plt.show()

# 3
plt.title('Polarity Difference')
labels = ['Paid', 'Free']
sizes = [full_d[full_d['Type'] == 'Paid']['Sentiment_Polarity'].mean(), full_d[full_d['Type'] == 'Free']['Sentiment_Polarity'].mean()]
plt.ylabel('average')
plt.bar(labels, sizes, color=['royalblue', 'cornflowerblue'])
plt.show()

# 4
rating_avg = apps_data[['Category', 'Rating']].groupby('Category')['Rating']
df = pd.DataFrame()
df['STD of rating'] = rating_avg.std()
df['Avg of rating'] = rating_avg.mean()
df['Mode of rating'] = rating_avg.agg(lambda x: pd.Series.mode(x)[0])
df['Median of rating'] = rating_avg.median()
print('--print-')
table = df[['Mode of rating', 'Median of rating', 'Avg of rating']]
df.plot(kind='bar', figsize=(20, 20), fontsize=5, width=1)
plt.show()

# 5
norm = table[(table['Avg of rating']<=table['Median of rating']+0.25) &(table['Avg of rating']>=table['Median of rating']-0.25)
&(table['Avg of rating']<=table['Mode of rating']+0.25)&(table['Avg of rating']>=table['Mode of rating']-0.25)]
print('--norm---')
print(norm)
print(df['STD of rating'].min()) # photo frame

# visualize for the report free vs paid pop
# free = apps_data[apps_data['Type'] == 'Free']['Type'].count()
# paid = apps_data[apps_data['Type'] == 'Paid']['Type'].count()
# x = [ 'paid','Free']
# y = [ paid, free]
# plt.title("paid vs free")
# plt.ylabel('number of apps')
# plt.xlabel('paid/free')
# plt.bar(x, y)
# plt.show()
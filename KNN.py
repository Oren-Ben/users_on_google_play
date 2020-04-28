import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
from part_B_Data_Analysis import get_file

apps_data = get_file("apps.csv")
review_data = get_file('user_reviews.csv')



full_table = pd.merge(apps_data, review_data, on='App')    # join between the tables
full_table = full_table.dropna(subset=['Sentiment'], how='any')    # dropped all the rows with missing Sentiment

#  ---- transfer columns Price & Size to numeric + normalization
full_table['Size'] = full_table['Size'].replace(to_replace='Varies with device', value=None, regex=True)
full_table['Size'] = full_table['Size'].replace({'[kK]': '*1e3', '[mM]': '*1e6'}, regex=True).map(pd.eval).astype(float)   # convert M to 1000
full_table['Size'] = full_table['Size'] / full_table['Size'].max()  # normalization
full_table['Price'] = full_table['Price'].str.replace('$','').astype(float)   # delete $
full_table['Price'] = full_table['Price'] / full_table['Price'].max()   # normalization

#  ---- copy the columns to local variables
X = full_table[['App', 'Category', 'Rating', 'Size', 'Type', 'Price', 'Genres', 'Sentiment_Polarity', 'Sentiment_Subjectivity']].copy()
Y = full_table['Sentiment'].copy()

#  ---- choose rows
X = X.iloc[60000:]
Y = Y.iloc[60000:]

#   complete missing values
my_imputer = SimpleImputer(missing_values=np.nan, strategy="most_frequent")
X = pd.DataFrame(my_imputer.fit_transform(X))
X.rename(columns={0: "App", 1: "Category", 2: "Rating", 3: "Size", 4: "Type", 5: "Price", 6: "Genres", 7: "Sentiment_Polarity", 8: "Sentiment_Subjectivity"}, inplace=True)

#  Convert categorical values to indicators
X = pd.get_dummies(X, columns=['App','Category','Type','Genres'], prefix=['App','Category','Type','Genres'])
Y = pd.get_dummies(Y)

#  Split groups to train and test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.20)


#  K-Neighbors
model_range = list(range(1,21))
model_scores = []
for k in model_range:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    score = metrics.accuracy_score(Y_test, Y_pred)
    model_scores.append(score)
optimal_k = model_range[model_scores.index((max(model_scores)))]

acc = str(round(max(model_scores)*100,2)) + "%"

print("Best K: {}, Best Accuracy: {}".format(optimal_k, acc))

#  bar plot for each k and its accuracy
plt.bar(model_range, model_scores)
plt.xticks(np.arange(1, 21, step=1))
plt.title('K- accuracy')
plt.xlabel('Value of K for KNN')
plt.ylabel('% Accuracy')
plt.show()
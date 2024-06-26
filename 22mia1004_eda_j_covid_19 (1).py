# -*- coding: utf-8 -*-
"""22MIA1004_EDA-J-covid-19.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l8-vAqFbW8NyB1lgYGfTkBVlbIAEwMDe

**Loading Libraries and Data**

---
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
!pip install pandas matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import missingno as msno
!pip install plotly
!pip install minepy
!pip install skrebate
!pip install scikit-learn

df = pd.read_csv('/content/COVID-19 Coronavirus.csv',header=None)

df.rename(columns={0:'Country',
                      1:'Other names',
                      2:'ISO',
                      3:'Population',
                      4:'Continent',
                      5:'Total Cases',
                      6:'Total Deaths',
                      7:'TC1Mpop',
                      8:'TD1Mpop',
                      9:'Death percentage'},inplace=True)

df.drop(index=0,inplace=True)

df['Total Cases']=df['Total Cases'].fillna(0).astype(int)
df['Total Deaths']=df['Total Deaths'].fillna(0).astype(int)
df['TC1Mpop']=df['TC1Mpop'].fillna(0).astype(int)
df['TD1Mpop']=df['TD1Mpop'].fillna(0).astype(int)
df['Death percentage']=df['Death percentage'].fillna(0).astype(float)

#This data transformation was necessary due to incorrect variable names in the dataset.

"""Data Information"""

df

# Total Cases 1million pop vs Total Deaths 1 million pop

from matplotlib import pyplot as plt
df.plot(kind='scatter', x='TC1Mpop', y='TD1Mpop', s=32, alpha=.8)
plt.gca().spines[['top', 'right',]].set_visible(False)

# Total Cases vs Total Deaths

from matplotlib import pyplot as plt
df.plot(kind='scatter', x='Total Cases', y='Total Deaths', s=32, alpha=.8)
plt.gca().spines[['top', 'right',]].set_visible(False)

df.columns

df.info()

df=df.drop(['Other names','ISO'],axis=1)

#After this transformation, the table is a 225x8 data array, 6 features are numeric, 2 are categorical.

import matplotlib.pyplot as plt

# Data (assuming Death Percentage is available)
death_percentage = 5  # Replace with your data

# Calculate percentage of population that survived
population_survived = 100 - death_percentage

# Define labels and colors
labels = ['Survived Population', 'Deceased Population']
colors = ['green', 'red']

# Create the pie chart
plt.pie([population_survived, death_percentage], labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Death Percentage Distribution')
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Create the histogram
fig, ax = plt.subplots()
ax.hist(df['Total Cases'], bins=10)

# Customize the histogram
ax.set_xlabel('Values')
ax.set_ylabel('Frequency')
ax.set_title('Histogram')

# Show the histogram
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
categories = df['Death percentage'].value_counts().index.tolist()
counts = df['Population'].value_counts().tolist()[:218]
print(df.shape)
print(len(categories))
print(len(counts))

counts = counts[:218]
# Create the Pareto chart
fig, ax = plt.subplots()


cumulative_counts = [sum(counts[:i+1]) for i in range(len(counts))]
cumulative_percentage = [count / sum(counts) * 100 for count in cumulative_counts]

ax.bar(categories, counts, color='steelblue')
ax2 = ax.twinx()
ax2.plot(categories, cumulative_percentage, color='red', marker='D')

# Customize the Pareto chart
ax.set_xlabel('Categories')
ax.set_ylabel('Counts')
ax2.set_ylabel('Cumulative Percentage')
ax.set_title('Pareto Chart')

# Show the Pareto chart
plt.show()

#z-score
import pandas as pd

def calculate_z_scores(data_file):



  # Select only numeric columns (excluding 'Death percentage')
  numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
  numeric_cols.remove('Death percentage')  # Assuming this is not numeric

  # Create a copy to avoid modifying original data
  data_with_zscores = df.copy()

  # Calculate z-scores for each numeric column
  for col in numeric_cols:
    mean = data_with_zscores[col].mean()
    std = data_with_zscores[col].std()
    data_with_zscores['z-score_' + col] = (data_with_zscores[col] - mean) / std

  return data_with_zscores

# Replace 'your_data.csv' with the actual path to your CSV file
data_with_zscores = calculate_z_scores('/content/COVID-19 Coronavirus.csv')

# Print the DataFrame with added z-score columns
print(data_with_zscores)

"""**Execution of Data Analysis**

---


"""

df.describe()

"""**Missing Data**

---


"""

msno.bar(df, figsize = (16,5),color = "blue")
plt.show()

df.isnull().sum()

"""There are no missing values in the dataset, which means that there will be no distortion of information during the correlation analysis.

**Interaction of variables with each other**

---
"""

columns=['Population', 'Total Cases', 'Total Deaths',
       'TC1Mpop', 'TD1Mpop', 'Death percentage']

sns.set()
sns.pairplot(df[columns],height = 5 ,kind ='scatter',diag_kind='kde')
plt.show()

"""**Outliers**

---


"""

i=1
plt.figure(figsize=(15,25))
for feature in columns:
    plt.subplot(6,3,i)
    sns.boxplot(y=df[feature])
    i+=1

print(df.columns)

import pandas as pd
import numpy as np
from scipy.spatial import distance

# Define the features
features = ['Population', 'Total Cases', 'Total Deaths', 'TC1Mpop', 'TD1Mpop', 'Death percentage']
df[features] = df[features].apply(pd.to_numeric, errors='coerce')

# Calculate the mean of the features
mean = np.mean(df[features], axis=0)

# Calculate the covariance matrix of the features
covariance = np.cov(df[features].values.T)

# Calculate the Mahalanobis distance for each data point
distances = distance.cdist(df[features], [mean], 'mahalanobis', VI=np.linalg.inv(covariance))

# Set a threshold for identifying outliers
threshold = np.mean(distances) + 3 * np.std(distances)

# Find the indices of the outliers
outlier_indices = np.where(distances > threshold)[0]

# Print the outliers
print(df.iloc[outlier_indices])

#DB scan
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Define the features
features = ['Population', 'Total Cases', 'Total Deaths', 'TC1Mpop', 'TD1Mpop', 'Death percentage']
df[features] = df[features].apply(pd.to_numeric, errors='coerce')

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# Create the DBSCAN model
model = DBSCAN(eps=3.5, min_samples=10)

# Fit the model to the scaled data
model.fit(df_scaled)

# Get the cluster labels
labels = model.labels_

# Get the number of clusters (excluding noise points)
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

# Get the number of noise points
n_noise = list(labels).count(-1)

# Print the results
print("Estimated number of clusters: %d" % n_clusters)
print("Estimated number of noise points: %d" % n_noise)

# Get the indices of the outliers (labelled as -1)
outlier_indices = np.where(labels == -1)[0]

# Print the outliers
print(df.iloc[outlier_indices])

#K-means scan
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Define the features
features = ['Population', 'Total Cases', 'Total Deaths', 'TC1Mpop', 'TD1Mpop', 'Death percentage']

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# Create the K-means model
model = KMeans(n_clusters=3)

# Fit the model to the scaled data
model.fit(df_scaled)

# Get the cluster labels
labels = model.labels_

# Get the cluster centers
centers = model.cluster_centers_

# Print the cluster labels and centers
print("Cluster Labels:")
print(labels)
print("Cluster Centers:")
print(centers)

# Calculate the Euclidean distance from each point to its cluster center
distances = np.zeros_like(labels, dtype=float)
for i, label in enumerate(labels):
    center = model.cluster_centers_[label]
    point = df_scaled[i]
    distances[i] = np.linalg.norm(point - center)

# Set a threshold for identifying outliers
threshold = np.mean(distances) + 3 * np.std(distances)

# Find the indices of the outliers
outlier_indices = np.where(distances > threshold)[0]

# Print the outliers
print(df.iloc[outlier_indices])

#Local Outlier Factor
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor

# Define the features
features = ['Population', 'Total Cases', 'Total Deaths', 'TC1Mpop', 'TD1Mpop', 'Death percentage']

# Create the LOF model
model = LocalOutlierFactor(n_neighbors=15, contamination=0.1)

# Fit the model to the data
model.fit(df[features])

# Get the outlier scores
outlier_scores = model.negative_outlier_factor_

# Set a threshold for identifying outliers
threshold = -2.5

# Find the indices of the outliers
outlier_indices = np.where(outlier_scores < threshold)[0]

# Print the outliers
print(df.iloc[outlier_indices])

"""**Feature Selection**

---


"""

df.info()

#correlation table
df['TD1Mpop'] = pd.to_numeric(df['TD1Mpop'], errors='coerce')
df = df[df['TD1Mpop'].notnull()]
df = df.select_dtypes(include=["number"])
correlation = df.corr()
print(correlation['TD1Mpop'].sort_values(ascending = False),'\n')

"""**Feature Selection**

"""

#Pearson Correlation-Feature Selection
import pandas as pd
import numpy as np

# Define the features and target variable
features = ['Total Cases', 'Population','Death percentage','TD1Mpop','TC1Mpop']
target = 'Total Deaths'

# Calculate the Pearson correlation coefficients
correlation_matrix = df[features + [target]].corr().abs()

# Select the highly correlated features
threshold = 0.5
relevant_features = correlation_matrix[correlation_matrix > threshold][target].dropna().index.tolist()

# Print the selected features
print("Selected Features:")
print(relevant_features)

#correlation chart
k= 10
cols = correlation.nlargest(k,'TD1Mpop')['TD1Mpop'].index
print(cols)
cm = np.corrcoef(df[cols].values.T)
f , ax = plt.subplots(figsize = (14,12))
sns.heatmap(cm, vmax=.8, linewidths=0.01,square=True,annot=True,cmap='viridis',
            linecolor="white",xticklabels = cols.values ,annot_kws = {'size':12},yticklabels = cols.values)
plt.show()

"""There is a high correlation between the number of cases and the number of deaths, which is generally logical.

We can convert the table to a form where cluster analysis can be carried out. To do this, you need to remove the continent variable and make the country variable an index.
"""

#t test
import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import t

# Define the features and target variable
features = ['Total Cases', 'Population', 'Death percentage', 'TD1Mpop', 'TC1Mpop']
target = 'Total Deaths'

# Perform t-test for each feature
t_scores = []
p_values = []
for feature in features:
    feature_class_1 = df[df[target] == 0][feature]
    feature_class_2 = df[df[target] == 1][feature]
    t_score, p_value = ttest_ind(feature_class_1, feature_class_2)
    t_scores.append(t_score)
    p_values.append(p_value)

# Select the features with significant p-values
alpha = 0.05
n = df.shape[0]

# Calculate the critical t-value
critical_t = t.ppf(1 - alpha/2, n)

# Print the critical t-value
print("Critical t-value:", critical_t)

relevant_features = [feature for i, feature in enumerate(features) if p_values[i] < critical_t]

# Find the feature with the highest absolute t-score
max_t_score = max(t_scores, key=abs)
best_feature = features[t_scores.index(max_t_score)]

# Print the selected features, t-scores, and p-values
print("Selected Features:")
for i, feature in enumerate(relevant_features):
    print("Feature:", feature)
    print("T-score:", t_scores[i])
    print("P-value:", p_values[i])
    print()

# Print the best feature based on the highest absolute t-score
print("Best Feature based on t-score:", best_feature)

#chi square test
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# Define the contingency table
contingency_table = pd.crosstab(df['Total Cases'], df['Total Deaths'])

# Perform the chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# Print the test results
print("Chi-square statistic:", chi2)
print("P-value:", p_value)
print("Degrees of freedom:", dof)
print("Expected frequencies:", expected)

# Find the feature with the lowest p-value
min_p_value = np.argmin(p_value)
best_feature = df.columns[min_p_value]

# Print the best feature based on the lowest p-value
print("Best Feature based on p-value:", best_feature)

#Information Based Correlation

import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from minepy import MINE

# Define the features and target variable
features = ['Total Cases', 'Population', 'Death percentage', 'TD1Mpop', 'TC1Mpop']
target = 'Total Deaths'

# Calculate Mutual Information Gain
mi_scores = mutual_info_classif(df[features], df[target])

# Calculate Maximal Information Coefficient (MIC)
mine = MINE()
mic_scores = []
for feature in features:
    mine.compute_score(df[feature], df[target])
    mic_scores.append(mine.mic())

# Print the scores
print("Mutual Information Gain Scores:")
for i, feature in enumerate(features):
    print("Feature:", feature)
    print("Score:", mi_scores[i])
    print()

print("Maximal Information Coefficient (MIC) Scores:")
for i, feature in enumerate(features):
    print("Feature:", feature)
    print("Score:", mic_scores[i])
    print()

#FCBF
import pandas as pd
import numpy as np


# Define the features and target variable
X = df.drop(columns=['Total Deaths']).values
y = df['Total Deaths'].values

# Calculate the correlation matrix
corr_matrix = np.corrcoef(X.T)

# Initialize the selected features list
selected_features = []

# Iterate over each feature
for i in range(X.shape[1]):
    # Calculate the correlation between the current feature and the target variable
    corr_with_target = np.abs(np.corrcoef(X[:, i], y)[0, 1])
    print("Correlation with Target:")
    print(corr_with_target)

    # Calculate the average correlation with the already selected features
    avg_corr_with_selected = np.mean(np.abs(np.corrcoef(X[:, i], X[:, selected_features].T)))
    print("Average correlation with selected:")
    print(avg_corr_with_selected)

    # Check if the current feature satisfies the FCBF criterion
    if corr_with_target < avg_corr_with_selected:
        selected_features.append(i)

# Get the names of the selected features
feature_names = df.columns[selected_features]

# Print the selected features
print("Selected Features:")
for feature in feature_names:
    print(feature)

df

#FAST
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, cut_tree
from sklearn.metrics import silhouette_samples

df.dtypes
df = df.astype(np.float64)

# Function to compute dissimilarity matrix
def compute_dissimilarity(df):
    dist_mat = pdist(df)
    return dist_mat

# Function to perform hierarchical clustering
def perform_clustering(dist_mat):
    hc = linkage(dist_mat, method='complete')
    return hc

# Function to cut dendrogram into k clusters
def cut_dendrogram(hc, k):
    clusters = cut_tree(hc, n_clusters=k).flatten()
    return clusters

# Function to compute silhouette scores
def compute_silhouette_scores(df, clusters):
    sil_scores = []
    for i in range(df.shape[1]):
        samples = df.iloc[:, i].values.reshape(-1, 1)  # Reshape the samples into a 2D array
        sil_score = silhouette_samples(samples, clusters)
        sil_scores.append(sil_score)
    return sil_scores

# Function to perform FAST feature selection
def fast(df, k):
    # Compute dissimilarity matrix
    dist_mat = compute_dissimilarity(df)

    # Perform hierarchical clustering
    hc = perform_clustering(dist_mat)

    # Cut dendrogram into k clusters
    clusters = cut_dendrogram(hc, k)

    # Compute silhouette scores
    sil_scores = compute_silhouette_scores(df, clusters)

    # Select features with highest silhouette scores
    mean_sil_scores = [np.mean(sil_score) for sil_score in sil_scores]
    selected_features = sorted(range(len(mean_sil_scores)), key=lambda i: mean_sil_scores[i], reverse=True)[:k]

    return selected_features


# Perform FAST feature selection
k = 3
selected = fast(df, k)
print(selected)

selected_feature_names = df.columns[selected]
print(selected_feature_names)

#Relief
import random
import numpy as np
import pandas as pd

def relief_algorithm(X, y, k):
    n_instances, n_features = X.shape

    # Initialize feature scores for all features
    feature_scores = np.zeros(n_features)

    for i in range(n_instances):
        current_instance = X[i]

        # Find nearest hit instance from the same class
        hits = np.where(y == y[i])[0]
        nearest_hit = random.choice(hits)

        # Find nearest miss instance from a different class
        misses = np.where(y != y[i])[0]
        nearest_miss = random.choice(misses)

        # Update feature scores
        for j in range(n_features):
            feature_scores[j] += abs(current_instance[j] - X[nearest_hit][j])
            feature_scores[j] -= abs(current_instance[j] - X[nearest_miss][j])

    # Rank the features based on their scores
    ranked_features = np.argsort(-feature_scores)

    # Select the top scoring features
    selected_features = ranked_features[:k]

    return selected_features


# Define the target column
target_column = "Total Deaths"

# Separate the features and the target variable
X = df.drop(target_column, axis=1).values
y = df[target_column].values

# Set the number of top features to select
k = 3

# Apply the Relief algorithm
selected_features = relief_algorithm(X, y, k)

# Print the selected feature indices
print(selected_features)

# Get the names of the selected features
feature_names = df.columns[selected_features]

# Print the selected feature names
print(feature_names)
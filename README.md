# Movie Recommendation Engine Web App

## 1. Introduction

Recommender systems are unavoidable in our daily online journeys, be it listening songs on Spotify, watching movies on Netflix or shopping on Amazon. To put it generally, recommender systems are complex algorithms with the aim to "predict" ratings or preference a user would give to a particular item. Being a huge movie buff I have created my personal movie recommender engine. I will be using collaborative filtering technique which essentially makes predictions for a particular user based on users with similar tastes.

## 2. Aim

The goal was to build an end-to-end movie recommender engine along with a sophisticated front-end and deploy it on Google Cloud Platform.

## 3. Dataset

The data used for training the model is called ml-latest-small and is provided by GroupLens. Please follow the [link](https://grouplens.org/datasets/movielens/) to download the dataset. Following files are used for analysis and model training purpose:

1. ratings.csv: this files has 3 columns representing userID, movieID and ratings respectively. There are 100,000 ratings given to to 9,000 movies by 600 users within this file.

2. movies.csv: The file contains titles of other miscellaneous details pertaining to 9,000 movies that are rated in the ratings.csv.

## 4. Modeling

I have used algorithms from Scikit-Surprise Library to generate the model and predict 5 movies for users based on the inputs provided by the user. Highlights of the modeling tasks include:

1. Reduced the size of the data by eliminating movies rated by less than 50 users & users who have rated less than 50 movies.

2. Benchmarked Singular Value Decomposition (SVD), SlopOne, Non-negative Matrix Factorization (NMF), NormalPredictor, KNNBaseline, KNNBasic, KNNWithMeans, KNNWithZScore, BaselineOnly, CoClustering algorithms and selected KNNBaseline as it had highest RMSE score.

3. Saved the initial model using "pickle" library.

Further details about the modeling tasks can be found in [EDA_and_Model_Generation](EDA_and_Model_Generation.ipynb) notebook.

## 5. Web App

I have used flask framework web-app. The front-end is designed using HTML, Bootstrap4 & CSS for styling. Some highlights of the webapp:

1. If the user is already in the dataset the user will get recommendations for the movies from the dataset which the users has not rated using the pre-trained model.

2. If the user is new, the preferences entered by the user will be added to the ratings dataset, the model will be trained again and predictions will be generated. In addition, the user is assigned an unique id and saved in the users.csv to identify new users uniquely.

In-depth details about these functions can be found in the [helper](utils/helper.py) file in the utils folder.

## 6. Deployment

The web app is deployed on Google Cloud Platform. In order to use the web-app follow [Movie-Recommendation-Engine](https://recommendation-4996.uc.r.appspot.com)

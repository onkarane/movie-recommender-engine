"import the required libraries"
import pandas as pd
import pickle
from surprise import Dataset, Reader, trainset
from surprise import KNNBaseline
from collections import defaultdict

class Predictions:

    '''
    Class contains the functions to get the movie predictions
    for the user inputs.
    '''

    def __get_csv(fname):
        '''
        Function to read movie and ratings csv files from data folder
        
        INPUT:
            1. fname(string): name of the file to read
            
        OUTPUT:
            1. df(pandas dataframe): dataframe of required file
        '''
        #read the csv file
        filepath = './data/' + fname + '.csv'
        df = pd.read_csv(filepath)
        
        return df
    
    def __set_csv(movie_list, rating_list, email):
        '''
        Function to update the csv files if the user does not exist

        INPUT: 
            1. movie_list(list): list of movies entered by the user
            2.rating_list(list): list of ratings given to the movies
            3. email (string): email address for the user to save

        OUTPUT:
            None
        '''
        #get the old csv files
        movies = Predictions.__get_csv('movies')
        ratings = Predictions.__get_csv('ratings')
        users = Predictions.__get_csv('users')

        #calculate the user id
        user_id = ratings.userId.max() + 1

        #save the user
        users.loc[len(users.index)] = [user_id, email]

        #get the movie ids
        movie_id_list = movies[movies['title'] \
                        .isin(movie_list)]['movieId']\
                        .tolist()
        #conver to dataframe
        df = pd.DataFrame(columns=['movieId'])
        #append the values
        df['movieId'] = movie_id_list
        df['userId'] = user_id
        df['rating'] = rating_list
        #rearange
        df = df[['userId', 'movieId','rating']]
        #append
        ratings = ratings.append(df, ignore_index=True)
        
        #save all the updated files
        users.to_csv('./data/users.csv', index=False)
        ratings.to_csv('./data/ratings.csv', index=False)

    def __get_model():
        '''
        Function to load reccomendation model from the model folder
        
        INPUT: 
            None
        
        OUTPUT:
            1. model (ml model): ml model loaded from pickle file
        '''
        #load the model
        filepath = './model/model.pkl'
        with open(filepath, 'rb') as file:
            model = pickle.load(file)
            
        return model
    
    def __save_model():
        '''
        Function to save reccomendation model in the model folder
        
        INPUT: 
            None
        
        OUTPUT:
            None
        '''
        #get the train set
        trainset = Predictions.__get_trainset()
        #train the model
        kknB = KNNBaseline()
        #generate the model
        model = kknB.fit(trainset)

        filepath = './model/model.pkl'
        with open(filepath, 'wb') as file:
            pickle.dump(model, file)

    def __get_trainset():
        '''
        Function will create a trainset by reading the csv

        INPUT:
            None
        
        OUPUT:
            1. trainset(surprise-trainset): a trainset with latest updated values
        '''
        #get the csv
        ratings = Predictions.__get_csv('ratings')
        #define a reader
        min_rating = ratings.rating.min()
        max_rating = ratings.rating.max()
        #define reader
        ratings = ratings[['userId', 'movieId', 'rating']]
        reader = Reader(rating_scale=(min_rating, max_rating))
        data = Dataset.load_from_df(ratings, reader)

        #get the trainset
        trainset = data.build_full_trainset()

        return trainset

    def __get_testset():
        '''
        Function will create a surprise testset for predictions

        INPUT: 
            1. None

        OUTPUT:
            trainset(surprise-testset): testset with the values not in trainset
        '''
        #get the trainset
        trainset = Predictions.__get_trainset()
        #generate testset
        testset = trainset.build_anti_testset()

        return testset
    
    def __get_top_n():
        '''
        Function to generate the predictions & return top 5 predictions
        
        INPUT:
            None
            
        OUTPUT:
            1. top_n(dict): dictonary with top n predictions for each user
        '''
        n = 5
        #get model
        model = Predictions.__get_model()
        #get the testset
        testset = Predictions.__get_testset()

        #generate predictions
        predictions = model.test(testset)

        # First map the predictions to each user.
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))

        # Then sort the predictions for each user and retrieve the k highest ones.
        for uid, user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]
        
        return top_n

    def __get_predictions(email):
        '''
        Function to retrive predictions for specific user

        INPUT:
            1. email(string): email address of the user to get the user id
        
        OUTPUT:
             movie_title(list): list of movie titles
        '''
        #get the csv
        users = Predictions.__get_csv('users')
        movies = Predictions.__get_csv('movies')

        #get the user id
        user_id = users[users['email'] == email]['userId'] \
                    .tolist()[0]

        #get the predictions for all users
        top_n = Predictions.__get_top_n()
        #filter predictions
        pred_list = top_n[user_id]
        #extract movie ids
        movie_id_list = [p[0] for p in pred_list]

        #get the titles
        movie_title = movies[movies['movieId'].isin(movie_id_list)]['title'].tolist()

        return movie_title
    
    def get_titles():
        '''
        Function to provide the homepage options dropdown with 
        movie titles

        INPUT:
            None
        
        OUTPUT:
            1. titles(list): list of movie titles in movie.csv

        '''
        #get the movies file and then titles
        movies = Predictions.__get_csv('movies')
        titles = movies.title.tolist()

        return titles
    
    def check_user(movies, ratings, email):
        '''
        Function to check if the user exisit and perform the actions accordingly

        INPUT:
            1. movies(list): list of movies select by the user
            2. ratings(list): list of ratings given to the movies
            3. email(string): email address of the user to check if it exist
        
        OUPUT:
            None
        '''
        #get the csv
        users = Predictions.__get_csv('users')
        #check if exist
        if email not in users.email.tolist():
            #save the user
            Predictions.__set_csv(movies, ratings, email)
            #train and save the model
            Predictions.__save_model()
        
        titles = Predictions.get_predicted_titles(email)

        return titles
    
    def get_predicted_titles(email):
        '''
        Function to call the apropriate functions to return predictions for user

        INPUT:
            1. email(string): email address of the user
        
        OUTPUT:
            1. titles(list): list of predicted movie titles
        '''
        titles = Predictions.__get_predictions(email)

        return titles

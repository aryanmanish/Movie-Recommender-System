# importing pandas for csv file operations
import pandas as pd

# loading csv file in dataframe df
df=pd.read_csv('movie_dataset.csv', low_memory=False)

# printing dataframe's top 5 rows
df.head(5)

# printing the rows and columns of the dataframe
print(df.shape)

# printing all columns names exits in the dataframe
df.columns

# features taken for finding cosine similarity
# keywords: someone may use keywords to search for movies
# genres: someone may use genres to search for movies
# cast: someone may like the cast of movie and wanted to view more movies of that cast
# director: someone may like the movies made by a specific director
# so these are the essentails features to be taken into considerations 
# for making normalized vectors from them and finding cosine simalariy between them
features = ['keywords', 'genres', 'cast', 'director']

# iterating over each column in dataframe for the given features
# and if any cell has 'Nan' value , it will be replaced by ''
for feature in features:
    df[feature] = df[feature].fillna('')

# combine_feature function definition for genreating rows by combining all the features
def combine_features(row):
    return row['keywords']+" "+row['genres']+" "+row['cast']+" "+row['director']

# create a new column with the name 'combined_features' and call for combine_features function over the dataframe over y-axis i.e vertically i.e columns 
df['combined_features'] = df.apply(combine_features,axis=1)

# printing first 3 rows of combined_features columns
df['combined_features'].head(3)

# importing from scikit learn CountVecotorizer for creating features as a vector and cosine_similarity for finding similarity between them
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# cv is created as object of CountVectorizer 
cv = CountVectorizer()

# crearing count_matrix from combined_features column for 80% rows of i.e 4809*20% = 961
count_matrix = cv.fit_transform(df['combined_features'][962:])

# finding cosine_similary from the count_matrix
cosine_sim = cosine_similarity(count_matrix)

# printing the cosine matrix dimensions
# cosine_sim.shape

# get_title_from_index fuction to get title from index 
def get_title_from_index(index):
    return df[df.index == index]['original_title'].values[0]

# get_index_from_title fuction to get index from title 
def get_index_from_title(title):
    return df[df.original_title == title]['index'].values[0]

# for i in range(0,10):
#     movie_user_like = df['original_title'][i]
    
#     try:
#         movie_index = int(get_index_from_title(movie_user_like))
#     except:
#         continue
#     similar_movies = list(enumerate(cosine_sim[movie_index]))
    
#     sorted_similar_movies= sorted(similar_movies, key= lambda x:x[1], reverse=True)[1:6]
    
#     print("\nTop 5 Similar Movies for ",movie_user_like)
    
#     for movie in sorted_similar_movies:
#         print(get_title_from_index(movie[0])," ,",movie[1])


from tkinter import *

def show_data():
    txt.delete(0.0, 'end')
    movie = ent.get()
    movie_user_likes = movie
    try:        
        movie_index = get_index_from_title(movie_user_likes)
        print ('Movie Index of given movie : '+ movie_index)

        i=int(movie_index)
        Similar_movies = list( enumerate(cosine_sim[i]))

        sorted_similar_movies = sorted(Similar_movies,key = lambda x:x[1], reverse = True)


        i=0
        j=0
        List =[None]*10
        for element in sorted_similar_movies:
                #print(get_title_from_index(element[0]))

                s=get_title_from_index(element[0])
                List[j]=s
                j=j+1

                #t="\n"
                #txt.insert(0.0, s)
            #txt.insert(0.0, t)
                i=i+1
                if i>=10:
                    break
            
            
        for x in range(len(List) -1, -1, -1):
            t="\n"
            txt.insert(0.0, List[x])
            txt.insert(0.0, t)

            #txt.insert(0.0, s)
    except:
        txt.insert(0.0, movie+' movie is not in the dataset')
        
   
root=Tk()
root.geometry("720x600")
               
l1 = Label(root, text="Enter Movie name: ")
l2 = Label(root, text="Top Ten Suggtion For You: ")
               
ent =Entry(root)
            
l1.grid(row=0)
l2.grid(row=2)
               
ent.grid(row=0, column=1)
               
            
               
               
               
               
txt=Text(root,width=90,height=63, wrap=WORD)
txt.grid(row=3, columnspan=2, sticky=W)
               
btn=Button(root, text="Search", bg="purple", fg="white", command=show_data)
btn.grid(row=1, columnspan=2)
root.mainloop()
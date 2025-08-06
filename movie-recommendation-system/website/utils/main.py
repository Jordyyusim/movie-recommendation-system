import pandas as pd
from ast import literal_eval

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class recommend():
    def __init__(self):
        self.df = pd.read_csv("D:\\Dev\\movie-recommendation-system\\website\\utils\\tmdb_5000_movies.csv")
        self.features = ["genres", "keywords"]
        
        for feature in self.features:
            self.df[feature] = self.df[feature].apply(literal_eval)
            self.df[feature+'_new'] = self.df[feature].apply(self.get_list_feature)
            self.df[feature] = self.df[feature].apply(self.get_list)
        
        self.df["combined"] = self.df.apply(self.combined, axis=1)
        self.df["title_lower"] = self.df["title"].str.lower()
        self.df['runtime'] = self.df['runtime'].fillna(0).astype(int)
        self.cosine_sim_matrix = self.cosine_sim(self.df["combined"])
    
    def get_list_feature(self, item):
        if isinstance(item, list):
            return [i["name"].lower().replace(" ", "") for i in item]
            
        return []
    
    def get_list(self, item):
        if isinstance(item, list):
            return [i["name"] for i in item]
            
        return []

    def combined(self, item):
        return ' '.join(item["genres_new"]) + ' '.join(item["keywords_new"])
    
    def cosine_sim(self, item):
        count = TfidfVectorizer(stop_words='english')
        count_matrix = count.fit_transform(item)
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        
        return cosine_sim
    
    def top_picks(self):
        df_top = self.df[(self.df["vote_count"]>500) & (self.df["vote_average"]>8.0)].sort_values(by='vote_average', ascending=False)
        df_top = df_top[["title", "vote_average", "release_date", "genres"]]
        df_top = df_top[0:10].values.tolist()
        
        return df_top
    
    def main(self, title):
        title = title.lower()
        idx = self.df[self.df["title_lower"] == title]
        if idx.empty:
            return [], "Movie Doesn't Exist"
        idx = idx.index[0]
        sim_scores = self.cosine_sim_matrix[idx]
        sim_scores = list(enumerate(sim_scores))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        indices = sim_scores[1:6]
        indices = [i[0] for i in indices]
        
        info = self.df[self.df['title_lower'] == title][['title', 'release_date', 'runtime', 'vote_average', 'overview', 'genres', 'vote_count']].iloc[0]
        
        return self.df["title"].iloc[indices].tolist(), info
        
        # for i in indices:
        #     result.append(self.df['original_title'].iloc[i])
        
        # return result

rec = recommend()
# print(rec.main('Avatar'))
    
    
    
    
    
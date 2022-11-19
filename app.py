from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np


popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pts1.pkl','rb'))
books = pickle.load(open('books1.pkl','rb'))
similarity_scores =  pickle.load(open('similarity_scores1.pkl','rb'))

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/the_book_spot'
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jdisqjmqyuohdm:8ae04cc8944b2f821fcdbb4f729e5aa0c51cfa0ed465f7ef03d8f14111f48766@ec2-18-209-78-11.compute-1.amazonaws.com:5432/d3v3bf86878p97"
#db = SQLAlchemy(app)




@app.route("/")
def home():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['book-path'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values),
                           link=list(popular_df['book-link'].values)
                           )
                           



if __name__ =="__main__":
    app.run(debug=True, port=8000)
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
                           
@app.route("/recommender")
def post():
    return render_template('recommender.html')


@app.route("/recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]  # calculating index of a book
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[
                    0:6]  # similarity of 1984 book with other books

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['book-link'].values))

        data.append(item)
    print(data)
    return render_template('recommender.html',data=data)


if __name__ =="__main__":
    app.run(debug=True, port=8000)
from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np
import random


app = Flask(__name__)

popular_books = pickle.load(open('Popular_books_final_with_info.pkl','rb'))
similarity_scores = pickle.load(open('Similarity_score.pkl','rb'))
books = pickle.load(open('Books.pkl','rb'))
table = pickle.load(open('table.pkl','rb'))




@app.route('/')
def index():
    return render_template('index.html',
                           image = list(popular_books['Image-URL-M'].values),
                           book_name = list(popular_books['Book-Title'].values),
                           author = list(popular_books['Book-Author'].values),
                           votes = list(popular_books['NumberOfRatings'].values),
                           rating = list(popular_books['AverageRating'].values)
                          
                           )




@app.route('/recommend')
def recommend_ui():
    sample_books = random.sample(list(table.index), 10)  
    return render_template('recommend.html', suggestions=sample_books)




@app.route('/recommend_books', methods=['POST'])
def recommend():
    book_name = request.form.get('user_input')  

    if book_name not in table.index:
        return render_template('recommend.html', not_found=True)

    index = np.where(table.index == book_name)[0][0]
    similar_books = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:9]

    data = []
    for i in similar_books:
        book_info = books[books['Book-Title'] == table.index[i[0]]].drop_duplicates('Book-Title')
        if book_info.empty:
            continue  
        item = [
            book_info['Book-Title'].values[0],
            book_info['Book-Author'].values[0],
            book_info['Image-URL-M'].values[0]
        ]
        data.append(item)

    return render_template('recommend.html', data=data)



@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(debug=True)
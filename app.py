from flask import Flask, render_template
import pickle

top_50 = pickle.load(open('top_50.pkl', 'rb'))
app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name= list(top_50['Book-Title'].values),
                           author_name = list(top_50['Book-Author'].values),
                           img= list(top_50['Image-URL-M'].values),
                           votes= list(top_50['num_ratings'].values),
                           ratings= list(top_50['avg_ratings'].values)
                           
                           
                           )


if __name__ == '__main__':
    app.run(debug=True)
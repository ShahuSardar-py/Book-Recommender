from flask import Flask, render_template, request
import pickle
import numpy as np

top_50 = pickle.load(open('top_50.pkl', 'rb'))
pt= pickle.load(open('pt.pkl', 'rb'))
books= pickle.load(open('books.pkl', 'rb'))
sim_scores= pickle.load(open('sim_scores.pkl', 'rb'))
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

@app.route("/recommend")
def recommend_page():
    return render_template('recommend.html')

@app.route('/recommend-books', methods=['post'])
def recommend():
    book_name= request.form.get('book_name')
    index= np.where(pt.index==book_name)[0][0]
    similar_items= sorted(list(enumerate(sim_scores[index])), key= lambda x:x[1],reverse=True)[1:5]
    
    data=[]
    for i in similar_items:
        item=[]
        
        temp_df= books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)


    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
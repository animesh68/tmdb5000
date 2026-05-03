from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from recommender import recommend, movies

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

# 🔍 autocomplete
@app.route('/search')
def search():
    query = request.args.get('q', '').lower()

    results = movies[
        movies['title'].str.lower().str.contains(query)
    ]['title'].head(10).tolist()

    return jsonify(results)

# 🎬 recommendations
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie = request.json['movie']

    try:
        names, posters = recommend(movie)
        return jsonify({
            "names": names,
            "posters": posters
        })
    except:
        return jsonify({"error": "Movie not found"})

if __name__ == '__main__':
    app.run(debug=True)
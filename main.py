from demographic_filtering import output
from content_filtering import get_recommendations
from storage import all_articles, liked_articles, unliked_articles
from flask import Flask, jsonify
import itertools

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    return jsonify({
        "data": all_articles[0],
        "status": "Success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)

    return ({
        "status": "Success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    unliked_articles.append(article)
    all_articles.pop(0)

    return ({
        "status": "Success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[0],
            "lang": article[1],
            "url": article[2],
            "text": article[3]
        }

        article_data.append(_d)

    return jsonify({
        "data": article_data,
        "status": "Success"
    }), 200

@app.route("/recommended-articles")
def recommmeded_articles():
    all_recommend = []

    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommend.append(data)

    all_recommend.sort()
    all_recommend = list(all_recommend for all_recommend, _ in itertools.groupby(all_recommend))

    article_data = []    

    for recommend in all_recommend:
        _d = {
            "title": recommend[0],
            "lang": recommend[1],
            "url": recommend[2],
            "text": recommend[3]
        }

        article_data.append(_d)

    return jsonify({
        "data": article_data,
        "status": "Success"
    }), 200

if __name__ == "__main__":
    app.run()
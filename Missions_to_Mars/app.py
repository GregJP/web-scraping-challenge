from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask app
app = Flask(__name__)

# Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Root route
@app.route("/")
def index():
    mars_scrape = mongo.db.mars_scrape.find_one()
    return render_template("index.html", mars_scrape=mars_scrape)

# Scrape route
@app.route("/scrape")
def scrape():
    mars_scrape = mongo.db.mars_scrape
    mars_data = scrape_mars.scrape()
    mars_scrape.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
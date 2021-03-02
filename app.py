#app.py

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one() #
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data # This is the connection to the mongo database
    mars_data_scraped = scrape_mars.scrape() #This runs the scrape function and stores returned dict
    mars_data.update_many({}, mars_data_scraped, upsert=True) #this adds scraped data to mongo db
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

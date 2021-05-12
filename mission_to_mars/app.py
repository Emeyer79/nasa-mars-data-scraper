from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_marsv3

# Create an instance of our Flask app.
app = Flask(__name__)

app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mongo.db.mars_data
    mars_scr = scrape_marsv3.scrape()
    mars_data.update({}, mars_scr, upsert = True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
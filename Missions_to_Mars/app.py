from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars # python file name

# Create an instance of Flask 
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database 
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function 
@app.route("/scrape")
def scrape():

    # Run the scrape function
    # Call the name of your file then the name of the function in that file
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
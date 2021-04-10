#Importing the Libraries
from flask import Flask, request, render_template
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import requests
import pymongo

#Creating the Object of Flask
app = Flask(__name__)

#Here We are Just Rendering the Reference HTML Pages
@app.route("/reference", methods=['GET'])
def reference():
    return render_template("reference.html")

#Here We are Just recieving the Search keyword from HTML form
#And then we are extracting the result of flipkart search with that query
#Now, After Search we are extracting the link of searched product and extracting the HTML tags with the Help of BeautifulSoup
#Now, We are find the the comment box and lopping through first 3 comments and extracting the information
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_string = request.form['content'].replace(" ", "+")
        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string #Just Making the URL with Search String
            flipkart_page = requests.get(flipkart_url)                          #Getting the Page Content
            flipkart_html = bs(flipkart_page.text, "html.parser")               #Converting teh Page content into HTML tags format
            product_boxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})  #Finding the Product Boxes
            first_box = product_boxes[3]                                        # Selecting the Third Product of above mentioned Class as first 3 may be useless
            product_url = "https://www.flipkart.com" + first_box.div.div.div.a['href'] #Now Getting the Product URL
            product_page = requests.get(product_url)                            #Getting the Content of Product page
            product_html = bs(product_page.text, 'html.parser')                 #Converting teh Page content into HTML tags format
            comment_boxes = product_html.findAll('div', {"class": "_16PBlm"})   #Now Finding the Comment Boxes or review Boxex

            reviews = []  # Empty List for Reviews

            #Here We are going through first 3 Comments and extracting information like, Name, Rating, Review
            for comment_box in comment_boxes[:3]:
                try :
                    rating = comment_box.div.div.div.div.text
                except:
                    rating = "No Ratings"
                try:
                    review_title = comment_box.div.div.p.text
                except:
                    review_title = "No Title"
                try:
                    reviewer_name = comment_box.findAll("p", {"class": "_2sc7ZR _2V5EHH"})[0].text
                except:
                    reviewer_name = "No Name"
                try:
                    rating_text = comment_box.div.div.div.next_sibling.text
                except :
                    rating_text = "No Review Text"

                #Creating the dictionary of all fetched details
                mydict = {"Product": " ".join(search_string.split("+")), "Name":reviewer_name, "Rating":rating
                        , "Title":review_title, "Review Text": rating_text}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews)

        except:
            return "Something is Wrong, Check with Admin, Please Send the Search Keywords to dr.deenukhan001@gmail.com"
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
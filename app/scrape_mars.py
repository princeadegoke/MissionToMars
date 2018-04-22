# Import Dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path":"chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # Empty dictionary to store the results
    mars={}

    browser = init_browser()
    nasamars_newsurl = "https://mars.nasa.gov/news/"
    # Visit the Nasa MARS News URL
    browser.visit(nasamars_newsurl)
    time.sleep(3)
    # Create a soup object to find the latest news from the URL
    html = browser.html
    news_soup = BeautifulSoup(html,"html.parser") 

    article = news_soup.find("div",class_="list_text")
    # Extract the date for which the news was posted
    mars["news_date"] = article.find("div",class_="list_date").text
    # Extract the title for which the news posted
    mars["news_title"] = article.find("div",class_="content_title").text
    # Extract the partial link for which the news posted
    link = article.find("div",class_="content_title").find("a").get("href")
    # Form the complete link by appending the strings with the partial link
    mars["news_link"] = "https://mars.nasa.gov" + link
    # Extract the article for which the news posted
    mars["news_p"] = article.find("div",class_="article_teaser_body").text

    # Mars JPL URL
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/"
    # Visit the JPL MARS URL
    browser.visit(jpl_url)
    time.sleep(3)
    # Create a soup object to find the latest news from the URL
    html = browser.html
    jpl_soup = BeautifulSoup(html,"html.parser") 

    img_link = jpl_soup.find("div",class_="carousel_container").find("div",class_="carousel_items").\
            find("article",class_="carousel_item").get("style").\
            split("('", 1)[1].split("')")[0]
    mars["featured_image_url"] = "https://jpl.nasa.gov"+img_link
    img_title = jpl_soup.find("div",class_="carousel_container").find("div",class_="carousel_items").\
            find("article",class_="carousel_item").find("h1",class_="media_feature_title").text.strip()
    mars["featured_image_title"] = img_title

    # Twitter Dependencies
    import tweepy
    import json

    # Twitter API Keys
    consumer_key = "md27jI2cdRGQ5QJrC9GrZnjfj"
    consumer_secret = "dp2ujQmPbGKDJO1UTx3S3kMdApXWz91XDMaLL1Ti92HygMrJVg"
    access_token = "943270787640852485-AMbIDMXo65N5tVrEPs5TJvVlU9c2faJ"
    access_token_secret = "lFoISe9o4VujzhvqWosuzWCS1uK2Ax7AeinI5r5mDsYG9"

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # Mars Twitter Weather URL
    marsweather_url="https://twitter.com/marswxreport?lang=en"
    # Visit the Mars Weather twitter page URL
    browser.visit(marsweather_url)
    time.sleep(3)
    # Create a soup object to find the latest news from the URL
    html = browser.html
    weather_soup = BeautifulSoup(html,"html.parser") 
    # Read the target_user from the URL
    target_user = "@" + weather_soup.find("b",class_="u-linkComplex-target").text
    # Read the recent tweet on the timeline
    mars_recentweather_tweet = api.user_timeline(target_user,count=1)
    mars["mars_weather"] = mars_recentweather_tweet[0]["text"]
    mars["mars_weather_url"] = marsweather_url

    
    # Import pandas to read the html page
    import pandas as pd

    # Mars Facts URL
    marsfacts_url = "https://space-facts.com/mars/"

    # Read the table from the html page
    table = pd.read_html(marsfacts_url)
    mars_data = table[0]
    mars_data = mars_data.rename(columns={0:"Parameter",1:"Value"})
    mars_data.set_index("Parameter",inplace=True)
    mars_data=mars_data.to_html()
    mars["mars_data"]=mars_data
    # Mars Hemisperes URL
    mars_hemisperes_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Visit the Mars Hemisperes URL
    browser.visit(mars_hemisperes_url)
    time.sleep(3)
    # Create a soup object to find the content from the URL
    html = browser.html
    hemisperes_soup = BeautifulSoup(html,"html.parser") 

    # Results from the first page that has all the four items
    hemisperes_results= hemisperes_soup.find("div",class_="collapsible results").find_all("div",class_="item")

    # Store the needed result  to a list
    hemisphere_image_urls=[] 
    for item in hemisperes_results:
        # Finding the title from the hemispere results
        title = item.find("h3").text
        # Visit the new URL upon clicking the thumbnail header or image
        url="https://astrogeology.usgs.gov"+item.find("a",class_="itemLink product-item").get("href")
        browser.visit(url)
        time.sleep(3)
        
        # Create a soup object to find the content from the URL with full size image
        html = browser.html
        img_soup = BeautifulSoup(html,"html.parser")

        # Extracting the parital link for the full sized image
        link = img_soup.find("div",class_="wide-image-wrapper").find("img",class_="wide-image").get("src")

        # Forming the entire link by appending the partial link
        img_url = "https://astrogeology.usgs.gov"+link

        # Append the result to the list
        hemisphere_image_urls.append({"title":title,"img_url":img_url,"hemisphere_url":url})

    mars["hemisphere_image_urls"]=hemisphere_image_urls
    
    # Return the results
    return mars
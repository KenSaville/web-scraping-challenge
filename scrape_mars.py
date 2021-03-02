#!/usr/bin/env python
#coding: utf-8

#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs 
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import requests
import pymongo


#initialize browser function

def init_browser():
    # Setup splinter
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path , headless=False)

# scrape function

def scrape():

    browser = init_browser()
    
    #define dictionary for storing values to return
    mars_data = {}

    #define initial url to be scraped and establish browser connection to this url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)  # to give browser time to load

    html = browser.html
    soup = bs(html, 'html.parser')

    # scrape news title and paragraph using bs
    all_news_titles=soup.find_all( class_ = "content_title")
    news_title = all_news_titles[1].text
    
    article_teasers = soup.find_all(class_='article_teaser_body')
    news_p = article_teasers[0].text

    #define next url to be scraped - for images
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # this url goes directly to larger image - no need to click to next page
    featured_image_url = soup.find_all('img', class_= 'BaseImage object-contain')[0]['data-src']
    
    # scrape new url using pandas, get table data from page
    url = 'https://space-facts.com/mars/'
    fact_table = pd.read_html(url)

    # set up dictionary contiaing hemisphere images from new page
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_unenhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_unenhanced.tif/full.jpg"}
        ]

    #add all scraped data to scraped_daa dict.  Return dict from function
    mars_data['News Title'] = news_title
    mars_data['News paragraph'] = news_p
    mars_data['Featured image url'] = featured_image_url
    mars_data['Mars Facts Table'] = fact_table
    mars_data['Hemispheres'] = hemisphere_image_urls

    return mars_data

#run function to see if it works to return dict
print(scrape())

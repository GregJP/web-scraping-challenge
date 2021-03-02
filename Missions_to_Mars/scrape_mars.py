from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # Setting up Chrome path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

mars_scrape = {}

def scrape():
    
    browser = init_browser()

    # News
    # Creating url variable and using BeautifulSoup to obtain webpage data
    nasa_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_news_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Pulling title and paragraph text from first article within url
    news_title = soup.find('div', class_ = 'list_text').find('div', class_ = 'content_title').text
    news_p = soup.find("div", class_ = "article_teaser_body").text

    mars_scrape['news_title'] = news_title
    mars_scrape['news_paragraph'] = news_p

    # Image
    # Creating url variable and using BeautifulSoup to obtain webpage data
    mars_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html#'
    browser.visit(mars_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Adding the url extension to the base url while also replacing the end of the base url
    featured_image_url = mars_image_url.replace('index.html#',(soup.find('img', class_='headerimage fade-in')['src']))
    
    mars_scrape['featured_image_url'] = featured_image_url

    # Facts
    # Using pandas to scrape table data from url
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)

    # Turning scraped table data into dataframe plus naming columns and setting index
    facts_df = facts_table[0]
    facts_df.columns = ['Description','Mars']
    facts_df.set_index('Description', inplace=True)

    facts_html = facts_df.to_html(justify='left')

    mars_scrape['facts_table'] = facts_html

    # Hemispheres
    # Creating url variable and using BeautifulSoup to obtain webpage data
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Creating variables to use in for loop
    hemispheres = soup.find_all('div', class_='item')
    hemi_info = []
    base_url = 'https://astrogeology.usgs.gov'

    # Setting up for loop to append title and url for each hemisphere as dictionary to list
    for hemi in hemispheres:
        
        # Scraping title text
        title = hemi.find('h3').text
        
        # Scraping image url for higher quality image
        base_img_url = hemi.find('a', class_='itemLink product-item')['href']
        
        # Using new image url with BeautifulSoup
        browser.visit(base_url + base_img_url)
        img_html = browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        
        # Adding high quality image url to base url
        img_url = base_url + soup.find('img', class_='wide-image')['src']
        
        # Adding both saved variables to dictionary and appending to list
        hemi_info.append({'title':title,'img_url':img_url})
    
    mars_scrape['hemispheres'] = hemi_info

    browser.quit()

    return mars_scrape
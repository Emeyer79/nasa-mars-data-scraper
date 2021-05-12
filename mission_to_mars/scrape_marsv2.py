from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'C:/webdrivers/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #Store as a dictionary all

    
def scrape():
    browser = init_browser()
    
    mars_data = {
        "news_title": title,
        "news_paragraph": first_p,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        "mars_facts": html_table,
        "hemispheres": hem_img_urls
        }
    
    return mars_data
    
  #------------title/paragraph------------------#

def title(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    #Use soup to scrape
    html = browser.html
    soup = bs(html, 'html.parser')

    #search for titles
    titles = soup.find_all ('div', class_ ='content_title')
    
    title = titles[1].text
    
    return title
    
def first_p(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
       
    #Use soup to scrape
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # p text for titles
    p_res = soup.find_all('div', class_='article_teaser_body')
    
    first_p = p_res[0].text
    
    return first_p
    
    #-----Find the feature image-------
    
    # Open browser to JPL Featured Image
def featured_image_url(browser):
    url = 'https://www.spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Click through to find full image
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Click again for full large image
    time.sleep(2)
    
    # browser.click_link_by_text('more info')
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for image source
    results = soup.find('img', class_='fancybox-image').get('src')
    featured_img_url = 'https://www.spaceimages-mars.com/' + results
    
    return featured_img_url
    
    #-----Mars Weather-------
    
    
def mars_weather(browser):
    
    #Open browser to Mars TW
    browser.visit('https://twitter.com/marswxreport?lang=en')
    
    # Parse the resulting html with soup
    html = browser.html
    tw_soup = bs(html, 'html.parser')

    #Search for tweets
    tweets = tw_soup.find_all(class_= "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")

    #Grab first tweet
    mars_weather = tweets[7].text
    
    return mars_weather
    
    #-----Mars Facts-----------
    
def html_table(browser):
    
    #Convert to a dataframe
    tables = pd.read_html('https://space-facts.com/mars/')

    #Pull the correct table
    df=tables[1]
    
    #Convert to html

    html_table = df.to_html(classes='data table table-borderless', index=False, header=False, border=0)
    
    return html_table
    
    
    #---------Hemispheres----------
    
def hem_img_urls(browser):
    
    #open page
    hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)
    
    #Search for titles
    html = browser.html
    hem_soup = bs(html, 'html.parser')

    names = []

    results = hem_soup.find_all('div', class_='collapsible results')
    hemispheres = results[0].find_all('h3')


    for name in hemispheres:
        names.append(name.text)
        
    #get the full sized images
    img_results = results[0].find_all('a')
    links = []

    for image in img_results:
        if (image.img):
        
            #getting the link
            img_url = 'https://astrogeology.usgs.gov/' + image['href']
        
            #append to to main url
            links.append(img_url)
            
    #get full sized image
    full_img = []

    #loop through and grab all image URLs
    for url in links:
    
        browser.visit(url)
    
        html = browser.html
        img_soup = bs(html, 'html.parser')
    
        results = img_soup.find_all('img', class_='wide-image')
        img_path = results[0]['src']
    
        img_link = 'https://astrogeology.usgs.gov/' + img_path
    
        full_img.append(img_link)
        
    #store as a dict

    #zip links
    zip_links = zip(names, full_img)


    #Create an empty list
    hem_img_urls = []


    #loop through zip and create dict
    for title, img in zip_links:
        url_dict = {}
        url_dict['title'] = title
        url_dict['img_url'] = img
    
    #append all together
    hem_img_urls.append(url_dict)
    
    return hem_img_urls
    
    
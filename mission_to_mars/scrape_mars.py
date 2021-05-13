from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'C:/webdrivers/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    
    #Open NASA news site
    browser.visit('https://mars.nasa.gov/news/')
    
    #Use soup to scrape
    html = browser.html
    soup = bs(html, 'html.parser')

    #search for titles
    titles = soup.find_all ('div', class_ ='content_title')

    # p text for titles
    p_res = soup.find_all('div', class_='article_teaser_body')

    #extract first title/p assign 
    first_title = titles[1].text
    first_p = p_res[0].text
    
    
    #-----Find the feature image-------
    
    # Open browser to JPL Featured Image
    browser.visit('https://www.spaceimages-mars.com/')
    
    # Click through to find full image
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    
    # browser.click_link_by_text('more info')
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for image source
    results = soup.find('img', class_='fancybox-image').get('src')
    featured_img = 'https://www.spaceimages-mars.com/' + results
    
    
    #-----Mars Facts-----------
    
    #Convert to a dataframe
    tables = pd.read_html('https://space-facts.com/mars/')

    #Pull the correct table
    df=tables[1]
    
    #Convert to html

    html_table = df.to_html(classes='data table table-borderless', index=False, header=False, border=0)
    
    
    #---------Hemispheres----------
    
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
    
    #Store as a dictionary all
    
    mars_data = {
        "news_title": first_title,
        "news_paragraph": first_p,
        "featured_image": featured_img,
        "mars_facts": html_table,
        "hemispheres": hem_img_urls
    }
    
    browser.quit()
    return mars_data



    


    
    

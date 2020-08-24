# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)   

def scrape():
    # NASA Mars News
    browser_news = init_browser()
    mars = {}

    news_url = 'https://mars.nasa.gov/news'
    browser_news.visit(news_url)

    # Find news title and news snippet paragraph
    html_news = browser_news.html
    soup_news = BeautifulSoup(html_news, 'html.parser')
    
    news_title = soup_news.find('div', class_='list_text').find('div', class_='content_title').text
    
    news_p = soup_news.find('div', class_='list_text').find('div', class_='article_teaser_body').text

    # Close the browser after scraping
    browser_news.quit()

    # ------------------------------------------------------------------------------------------------
    # JPL Mars Space Images - Feature Image
    browser_feature = init_browser()

    feature_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser_feature.visit(feature_url)

    # Find the featured image
    html_feature = browser_feature.html
    soup_feature = BeautifulSoup(html_feature, 'html.parser')

    featured_image_url = soup_feature.find('div', class_='carousel_items').find('footer').find('a', class_='button fancybox')['data-fancybox-href']

    featured_image_url = (f'https://www.jpl.nasa.gov{featured_image_url}')

    # Close the browser after scraping
    browser_feature.quit()

    # ------------------------------------------------------------------------------------------------
    # Mars Facts
    
    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    
    # Create dataframe of table
    mars_df = mars_facts[0]

    # Rename Columns
    mars_df = mars_df.rename(columns={0:"Description", 1:"Mars"})

    # Set Index
    mars_df.set_index("Description", inplace=True)

    # Create HTML table / Convert dataframe to HTML
    mars_html_table = mars_df.to_html()

    # Remove \n (new lines)
    mars_html_table.replace('\n', '')

    # ------------------------------------------------------------------------------------------------
    # Mars Hemispheres
    browser_hemisphere = init_browser()

    hemisphere_list = ['cerberus', 'schiaparelli', 'syrtis_major', 'valles_marineris']

    hemisphere_image_urls = []

    for x in hemisphere_list:
        hemisphere_url = (f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{x}_enhanced')
        browser_hemisphere.visit(hemisphere_url)
            
        html_hemisphere = browser_hemisphere.html
        soup_hemisphere = BeautifulSoup(html_hemisphere, 'html.parser')
            
        content = soup_hemisphere.find('div', class_='content')
        title = content.find('h2').text
        image_url = content.find('a')['href']
        
        hemisphere_image_urls.append({'title':title, 'img_url':image_url})

    # Close the browser after scraping
    browser_hemisphere.quit()

    # ------------------------------------------------------------------------------------------------
    # Create final dictionary
    mars["news_title"] = news_title
    mars["news_p"] = news_p
    mars["featured_image_url"] = featured_image_url
    mars["mars_facts"] = mars_html_table
    mars["hemisphere_image_urls"] = hemisphere_image_urls

    return mars

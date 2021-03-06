
# Import dependencies
import pandas as pd
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time


# In[181]:


# Configure ChromeDriver
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path)


# # NASA Mars News


# In[192]:


def mars_news():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    time.sleep(3) # Sleep for 3 seconds

    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    article_container = news_soup.find('ul', class_='item_list')

    headline_date = article_container.find('div', class_='list_date').text
    headline_date
    
    news_title = article_container.find('div', class_='content_title').find('a').text
    news_p = article_container.find('div', class_='article_teaser_body').text

    return news_title, news_p


# # JPL Mars Space Images - Featured Image

# In[222]:


def featured_image():
    base_url = 'https://www.jpl.nasa.gov'

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    
    # Method of clicking the FULL TEXT button and pulling the image
    try:
        full_image_elem = browser.find_by_id('full_image')[0]
        full_image_elem.click()

        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')

        img_rel_url = img_soup.find('img', class_='fancybox-image')['src']
        
    except Exception as e:
        print(e)

    featured_image_url  = f'{base_url}{img_rel_url}'
      
    return  featured_image_url


# # Mars Facts

# In[224]:


def mars_facts():
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    mars_facts_df = pd.read_html(url)
    mars_facts_df = mars_facts_df[0]
    mars_facts_df.columns = ['Description', 'Mars']
    mars_facts_df

    mars_facts_html = mars_facts_df.to_html(classes='table table-striped')
    
    return mars_facts_html


# # Mars Hemispheres

# In[230]:


def mars_hemispheres():    
    # Retrieve page with the requests module 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url) 

    html = browser.html  

    #Use Beautiful soup to find Hemisphere titles in text

    elements_soup = BeautifulSoup(html, 'html.parser')
    elements_div = elements_soup.find("div", class_ = "collapsible")
    elements = elements_div.find_all("h3")
    elements = [element.text for element in elements]
    elements

    # Use Splinter to click each title and scrap for the full hemisphere image  

    hemisphere_image_urls = [] 

    # empty list to be appended by dictionaries  

    for x in range(len(elements)): 

        #parse for each title element          

        browser.links.find_by_partial_text(f'{elements[x]}').click()          
       
        title = elements[x]     

        image_url = browser.find_by_css('a').links.find_by_partial_text("Sample")['href']          

        hemisphere_image_urls.append(                                 
        {"title": f'{title}', "img_url": f'{image_url}'}
                                    )
        #return to home page
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
       
        html = browser.html
        
    return hemisphere_image_urls



# # Insert into Mongo DB

# In[232]:


def scrape_all():

    # Populate variables from the functions
    news_title, news_p = mars_news()
    featured_img_url = featured_image()
    mars_facts_html = mars_facts()
    hemispheres_mars= mars_hemispheres()

    # Assemble the document to insert into the database
    nasa_document = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_url': featured_img_url,
        'mars_facts': mars_facts_html,
        'hemispheres': hemispheres_mars
    }

    return nasa_document


# In[234]:
#Run Script

if __name__ == "__main__":
    scrape_all()



# In[ ]:





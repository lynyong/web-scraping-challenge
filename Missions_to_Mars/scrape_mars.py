# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import datetime as dt

def scrape_all():
    # Set up executable path
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": facts(),
        "hemisphere": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data

# NASA Mars News
def mars_news(browser):

    # Set up url
    nasa_url = "https://mars.nasa.gov/news/"
    # Opens the website via pop-up browser 
    browser.visit(nasa_url)

    # Retrieve HTML of the browser 
    html = browser.html
    # Parse HTML with Beautiful Soup 
    soup = BeautifulSoup(html, "html.parser")

    # Add try/except for error handling
    try:
        results = soup.select_one("ul.item_list li.slide")

        # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
        news_title = results.find("div", class_="content_title").text
        news_p = results.find("div", class_="article_teaser_body").text
    except AttributeError:
        return None, None
    return news_title, news_p

# JPL Space Images Featured Image
def featured_image(browser):

    # Set up url
    jpl_url_root = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    # Opens the website via pop-up browser 
    browser.visit(jpl_url)

    # Click full image and more info to get image url
    full_image_button = browser.links.find_by_partial_text('FULL IMAGE')
    full_image_button.click()

    # Retrieve HTML of the browser 
    image_html = browser.html
    # Parse HTML with Beautiful Soup 
    img_soup = BeautifulSoup(image_html, 'html.parser')

    # Find the image url
    full_image_url = img_soup.select_one('img.fancybox-image').get("src")
    featured_image_url = jpl_url_root + full_image_url
    return featured_image_url

# Mars Facts
def facts(): 

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    facts_df.columns = ["Description", "Mars"]
    facts_df.set_index("Description", inplace = True)
    facts_df

    # Use Pandas to convert the data to a HTML table string.
    return facts_df.to_html(classes="table table-striped")

# Mars Hempispheres
def hemisphere(browser):

    # # Set up url
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Opens the website via pop-up browser 
    browser.visit(usgs_url)

    hemisphere_image_urls = []

    #  Get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")

    for i in range(4):
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)
        # Navigate backwards
        browser.back()
    return hemisphere_image_urls

def scrape_hemisphere(html_text):
    # Parse html text
    hemi_soup = BeautifulSoup(html_text, "html.parser")
    # Add try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")
    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None
    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }
    return hemispheres

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
    



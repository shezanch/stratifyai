#Fucntions for agent to use
import requests 
from bs4 import BeautifulSoup

#Menu Option 1
def get_user_input():
    while True:

        user = input("Enter website to analyze: ") #Takes input from user
        user = user.strip()
        
    #Input Validations
        if user == "": #Did the user type anything at all
            print ("You must enter a website")
            continue
        
        elif not user.startswith("http://") and not user.startswith("https://"): #Does it look like a URL?
            print ("You must enter a valid website starting with http:// or https://")
            continue

        return user

#Menu option 2
def get_niche_input(): #Gets niche entered by user
     while True:
          user_niche = input("Enter a niche: ")
          user_niche = user_niche.strip()

          #Input validations
          if user_niche == "":
               print("You must enter a niche")
               continue
          else:
            return user_niche
        
     
def web_catcher (url): #Function to analyze a given website

    try:

        response = requests.get(url, timeout=10) #goes to the webpage and downloads it 
    
    except:
        return "Enter a valid website"
    
    else: 
        errors = { 403: "Website blocked the scraper",
                  404: "Website page not found",
                  500: "Website server error"}
        
        if response.status_code == 200:
        
            html = response.text #HTML code from downloaded page
            soup = BeautifulSoup(html, "html.parser") #understands HTML like a webpage structure
            
            cleaner = web_cleaner(soup)

            content = validate_content(cleaner)
            return content
        
        elif errors.get(response.status_code):
             return errors.get(response.status_code)
        else:
             return "Website returned unexpected status code"

    
def web_cleaner(soup): #Website content cleaner
        for tag in soup (["script","style","nav","footer","header","aside","form","button"]):
            tag.decompose()
        
        cleaned_text = soup.get_text(separator="\n") #extracts all visible text and separates sections with new lines

        lines = cleaned_text.splitlines() #splits the big text block into individual lines

        cleaned_lines = [] #creates an empty set 
        for x in lines:
             x = x.strip() # removes extra spaces from the start and end of the line
             word_count = len(x.split()) # counts how many words are in this line
             if word_count > 3:
                  cleaned_lines.append(x) 

        final_text = "\n".join(cleaned_lines)
        return final_text

def validate_content(cleaner): #website validation function
        count_char = len(cleaner)
        if cleaner.strip() == "":
            return "Website appears to be blank"
        elif count_char <= 200:
            return "Website does not have meaningful information"
        return cleaner #returns value of soup

def get_trending_topics(niche):
    cleaned_niche = niche.replace(" ", "+")
    google_url = f"""https://news.google.com/rss/search?q={cleaned_niche}&hl=en-US&gl=US&ceid=US:en"""
    try:
        niche_response = requests.get(google_url, timeout=10)
    except:
        return "Google blocked your request"
    else:
        errors = { 403: "Google News blocked the scraper",
                404: "Google News page not found",
                500: "Google News server error"}
        if niche_response.status_code == 200:
            niche_xml = niche_response.text
            soup = BeautifulSoup(niche_xml, "xml")

            titles = []
            items = soup.find_all("item")
            for item in items:
                headline = item.find("title")
                if headline is not None: 
                    headline_text = headline.text
                    titles.append(headline_text)

            return titles[:10]
        
        elif errors.get(niche_response.status_code):
            return errors.get(niche_response.status_code)
        else:
            return "Google News returned unexpected status code"



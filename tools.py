#Fucntions for agent to use
import requests 
from bs4 import BeautifulSoup


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


        
     
def web_catcher (url): #Function to analyze a given website

    try:

        response = requests.get(url) #goes to the webpage and downloads it 
    
    except:
        return "Enter a valid website"
    
    else: 
        if response.status_code == 403:
            return "Website blocked the scraper"
        elif response.status_code == 404:
             return "Website page not found"
        elif response.status_code == 500:
             return "Website server error"
        elif response.status_code == 200:
        
            html = response.text #HTML code from downloaded page
            soup = BeautifulSoup(html, "html.parser") #understands HTML like a webpage structure
            
            cleaner = web_cleaner(soup)

            content = validate_content(cleaner)
            return content

    
def web_cleaner(soup):
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

def validate_content(cleaner):
        count_char = len(cleaner)
        if cleaner.strip() == "":
            return "Website appears to be blank"
        elif count_char <= 200:
            return "Website does not have meaningful information"
        return cleaner #returns value of soup


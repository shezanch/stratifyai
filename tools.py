#Fucntions for agent to use
import requests 
from bs4 import BeautifulSoup


def web_catcher (url): #Function to analyze a given website

    try:

        response = requests.get(url) #goes to the webpage and downloads it 
    
    except:
        return "Enter a valid website"
    
    else: 
        if response.status_code != 200:
            return "Website not found"
        
        html = response.text #HTML code from downloaded page
        soup = BeautifulSoup(html, "html.parser") #understands HTML like a webpage structure
        return soup.text #returns value of soup
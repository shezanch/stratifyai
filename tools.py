#Fucntions for agent to use
import requests 
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv #Reads necessary values from .env (in this case API Key)
from google.api_core.exceptions import *

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY")) #API Key configured once. Uses this api key from .env whenever gemini is called

model = genai.GenerativeModel("gemini-3-flash-preview") #Specifies which model of gemini api to use

#Menu Option 1
def get_user_input():

    user = input("Enter website to analyze: ") #Takes input from user
    user = user.strip()
    
#Input Validations
    if user == "": #Did the user type anything at all
        print ("You must enter a website")
       
    
    elif not user.startswith("http://") and not user.startswith("https://"): #Does it look like a URL?
        print ("You must enter a valid website starting with http:// or https://")
        

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

def get_platform_input():
    print("1. Linkedin")
    print("2. Instagram")
    print("3. Tiktok")
    user_platform = input("Enter a platform:")
    if user_platform == "":
        print ("You must enter a platform: ")
        
    elif user_platform == "1":
        user_platform = "Linkedin"
        
    elif user_platform == "2":
        user_platform = "Instagram"
        
    elif user_platform == "3":
        user_platform = "Tiktok"

    return user_platform

def get_tone_input():
    print("1. Professional")
    print("2. Casual")
    print("3. Funny")

    tone_input = input("Enter tone: ")
    if tone_input == "":
        print("You must enter a tone")
    elif tone_input == "1":
        tone_input = "Professional"
        
    elif tone_input == "2":
        tone_input = "Casual"
        
    elif tone_input == "3":
        tone_input = "Funny"
    
    return tone_input

    
     
def web_catcher (url): #Function to analyze a given website
    url = url.strip()
    try:

        response = requests.get(url, timeout=10) #goes to the webpage and downloads it 
    
    except requests.exceptions.Timeout:
        return "The website took too long to respond"

    except requests.exceptions.InvalidURL:
        return "The website URL is invalid"

    except requests.exceptions.TooManyRedirects:
        return "The website redirected too many times"

    except requests.exceptions.ConnectionError:
        return "StratifyAI could not connect to the website"

    except requests.exceptions.RequestException:
        return "StratifyAI could not retrieve the website"
    
    else: 
        errors = {403: "Website blocked the scraper",
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
    niche = niche.strip()
    cleaned_niche = niche.replace(" ", "+")
    google_url = f"""https://news.google.com/rss/search?q={cleaned_niche}&hl=en-US&gl=US&ceid=US:en"""
    try:
        niche_response = requests.get(google_url, timeout=10)
    except requests.exceptions.Timeout:
        return "Google News took too long to respond"

    except requests.exceptions.ConnectionError:
        return "StratifyAI could not connect to Google News"

    except requests.exceptions.TooManyRedirects:
        return "Google News redirected too many times"

    except requests.exceptions.RequestException:
        return "StratifyAI could not retrieve trending topics"
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
        
        
def get_url_strategy(website):
        prompt = f"""You are a social media content strategist.
        A user has given you the content from a website.
        Your job is to:
        1. Summarize what this website/page is about in 2-3 sentences
        2. Identify 3 content ideas inspired by this page that would perform well on social media
        3. For each idea write a short caption and 5 hashtags

        Website text:
        {website}
        """
        try:
            response = model.generate_content(prompt)
        except ResourceExhausted:
            return "The AI usage limit has been reached. Please try again later"

        except InvalidArgument:
            return "StratifyAI could not process the request. Please review your inputs"

        except Unauthenticated:
            return "The AI service could not authenticate. Please check the API key"

        except PermissionDenied:
            return "StratifyAI does not have permission to use the AI service"

        except DeadlineExceeded:
            return "The AI response took too long. Please try again"

        except ServiceUnavailable:
            return "The AI service is temporarily unavailable. Please try again shortly"

        except InternalServerError:
            return "The AI service encountered an internal error. Please try again later"

        except GoogleAPICallError:
            return "StratifyAI could not complete the AI request. Please try again"
        else:
            return response.text

def get_niche_strategy(topics, niche, platform, tone, day_numbers):
    niche_prompt = f"""You are a social media content strategist. The user's niche is {niche} and they are creating content for {platform} with a {tone} tone. 
    Here are the current trending headlines in this niche: {topics}. 
    Using these trends as inspiration, generate the following: first a trend summary in 2-3 sentences explaining what is happening in this niche right now, 
    then a {day_numbers}-day content calendar. For each day provide the day number as a header, a punchy one-line post hook, a full caption written specifically for 
    {platform} in a {tone} tone, and exactly 5 relevant hashtags. Keep each day clearly separated. Do not add any filler, introductions, or closing remarks — 
    just the structured output.
    """
    try:
        response = model.generate_content(niche_prompt)
    except ResourceExhausted:
        return "The AI usage limit has been reached. Please try again later"

    except InvalidArgument:
        return "StratifyAI could not process the request. Please review your inputs"

    except Unauthenticated:
        return "The AI service could not authenticate. Please check the API key"

    except PermissionDenied:
        return "StratifyAI does not have permission to use the AI service"

    except DeadlineExceeded:
        return "The AI response took too long. Please try again"

    except ServiceUnavailable:
        return "The AI service is temporarily unavailable. Please try again shortly"

    except InternalServerError:
        return "The AI service encountered an internal error. Please try again later"

    except GoogleAPICallError:
        return "StratifyAI could not complete the AI request. Please try again"
    
    else:
        return response.text



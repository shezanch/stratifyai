#Main loop
import google.generativeai as genai
import os
from dotenv import load_dotenv #Reads necessary values from .env (in this case API Key)
from tools import *
from google.api_core.exceptions import ResourceExhausted


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY")) #API Key configured once. Uses this api key from .env whenever gemini is called

model = genai.GenerativeModel("gemini-2.5-flash") #Specifies which model of gemini api to use

while True:
    print ("================================ Welcome to StratifyAI ================================")

    print ("1. Enter Url")
    print ("2. Enter niche")

    
    menuOption = input ("Enter menu option: ")

    
    if menuOption == "1":
        url = get_user_input()
        website = web_catcher(url)
        error_messages = [ "Enter a valid website",
                "Website does not have meaningful information",
                "Website appears to be blank",
                "Website blocked the scraper",
                "Website page not found",
                "Website server error",
                "Website returned unexpected status code"]
        if website in error_messages:
            print(website)
            continue

        prompt = f"""You are a social media content strategist.
        A user has given you the content from a website.
        Your job is to:
        1. Summarize what this website/page is about in 2-3 sentences
        2. Identify 3 content ideas inspired by this page that would perform well on social media
        3. For each idea write a short caption and 5 hashtags

        Website text:
        {website}
        """

    elif menuOption == "2":
        niche = get_niche_input()
        topics = get_trending_topics(niche)

        error_messages = [ "Google News blocked the scraper",
                "Google News page not found",
                "Google News server error",
                "Google News returned unexpected status code"]
        if topics in error_messages:
            print(topics)
            continue
        elif topics == []:
            print ("No trending topics found")
            continue

        niche_prompt = f"""You are a social media content strategist.

        The user's niche is:
        {niche}

        Here are recent Google News headlines related to that niche:
        {topics}

        Use these headlines to generate:
        1. A short trend summary
        2. Five content ideas
        3. A 7-day content calendar
        4. Captions and hashtags
        """

    
    elif menuOption == "quit":
        break

    else:
        print ("Invalid menu option")
        continue


    try:
        if menuOption == "1":
            response = model.generate_content(prompt) #Generates a response based on user input
        elif menuOption == "2":
            response = model.generate_content(niche_prompt)
    except ResourceExhausted:
        print ("Api rate limit reached. Try again later")
    except:
        print ("ApI failed. Try again later")
    else:
        print ("AI:", response.text)
       
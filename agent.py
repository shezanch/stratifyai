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
    print ("================================ Welcome to your personal AI Agent ================================")

    print ("1. Enter Url")
    print ("2. Enter niche")

    
    menuOption = input ("Enter menu option: ")
    
    if menuOption == "1":
        url = get_user_input()
        website = web_catcher(url)


    
    elif menuOption == "2":
        print ("Feature still under development")
        continue
    
    elif menuOption == "quit":
        break

    else:
        print ("Invalid menu option")
        continue


    if website == "Enter a valid website": #Checks validation from tools if website is valid
        print (website)
        continue



    elif website == "Website does not have meaningful information":
        print (website)
        continue
    elif website == "Website appears to be blank":
        print (website)
        continue
    elif website == "Website blocked the scraper":
        print (website)
        continue
    elif website == "Website page not found":
        print (website)
        continue
    elif website == "Website server error":
        print (website)
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

    try:
        response = model.generate_content(prompt) #Generates a response based on user input
    except ResourceExhausted:
        print ("Api rate limit reached. Try again later")
    except:
        print ("ApI failed. Try again later")
    else:
        print ("AI:", response.text)
       
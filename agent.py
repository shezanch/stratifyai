#Main loop
import google.generativeai as genai
import os
from dotenv import load_dotenv #Reads necessary values from .env (in this case API Key)
from tools import web_catcher
from google.api_core.exceptions import ResourceExhausted


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY")) #API Key configured once. Uses this api key from .env whenever gemini is called

model = genai.GenerativeModel("gemini-2.5-flash") #Specifies which model of gemini api to use

while True:

    user = input("Enter website to analyze: ") #Takes input from user
    user = user.strip()
    
#Input Validations
    if user == "": #Did the user type anything at all
        print ("You must enter a website")
        continue

    elif user == "quit": #If user quits this breaks the loop
        break
    
    elif not user.startswith("http://") and not user.startswith("https://"): #Does it look like a URL?
        print ("You must enter a valid website starting with http:// or https://")
        continue

    
    website = web_catcher(user) #Calls the function and provides the URL value

    if website == "Enter a valid website": #Checks validation from tools if website is valid
        print (website)
        continue

    elif website == "Website not found":
        print (website)
        continue

    elif website == "Website does not have meaningful information":
        print (website)
        continue


    try:
        response = model.generate_content(website) #Generates a response based on user input
    except ResourceExhausted:
        print ("Api rate limit reached. Try again later")
    except:
        print ("ApI failed. Try again later")
    else:
        print ("AI:", response.text)
       
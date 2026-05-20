#Main loop
import google.generativeai as genai
import os
from dotenv import load_dotenv #Reads necessary values from .env (in this case API Key)
from tools import web_catcher

while True:

    load_dotenv()

    genai.configure(api_key=os.getenv("GEMINI_API_KEY")) #API Key configured once. Uses this api key from .env whenever gemini is called

    model = genai.GenerativeModel("gemini-2.5-flash") #Specifies which model of gemini api to use

    user = input("Enter website to analyze: ") #Takes input from user

    website = web_catcher(user) #Calls the function and provides the URL value

    response = model.generate_content(website) #Generates a response based on user input


    print ("AI:", response.text) #prints response 


    if user == "quit": #If user quits this breaks the loop
        break
import streamlit as st
from tools import *
import pandas as pd

#Session States
if 'generated_strategy' not in st.session_state:
    st.session_state.generated_strategy = None

if 'mode_result' not in st.session_state:
    st.session_state.mode_result = None

if 'platform_result' not in st.session_state:
    st.session_state.platform_result = None

if 'voice_result' not in st.session_state:
    st.session_state.voice_result = None

if 'days_result' not in st.session_state:
    st.session_state.days_result = None

if 'trend_headlines' not in st.session_state:
    st.session_state.trend_headlines = None

#Error messages
gemini_errors_messages = ["The AI usage limit has been reached. Please try again later",
"StratifyAI could not process the request. Please review your inputs",
"The AI service could not authenticate. Please check the API key",
"StratifyAI does not have permission to use the AI service",
"The AI response took too long. Please try again",
"The AI service is temporarily unavailable. Please try again shortly",
"The AI service encountered an internal error. Please try again later",
"StratifyAI could not complete the AI request. Please try again"]

url_error_messages = ["The website took too long to respond",
"The website URL is invalid",
"The website redirected too many times",
"StratifyAI could not connect to the website",
"StratifyAI could not retrieve the website",
"Website does not have meaningful information",
"Website appears to be blank",
"Website blocked the scraper",
"Website page not found",
"Website server error",
"Website returned unexpected status code"]

niche_error_messages = ["Google News took too long to respond",
"StratifyAI could not connect to Google News",
"Google News redirected too many times",
"StratifyAI could not retrieve trending topics",
"Google News blocked the scraper",
"Google News page not found",
"Google News server error",
"Google News returned unexpected status code"]


#Zen dots font 
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Zen+Dots&display=swap');

    .zen-title {
        font-family: 'Zen Dots', sans-serif;
        font-size: 60px;
        text-align: center;
        font-weight: 400;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#Tetktur font
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tektur:wght@400..900&display=swap');

    .tektur-body {
    font-family: "Tektur", sans-serif;

    }
    </style>
    """, unsafe_allow_html=True
)

#Header and tagline
st.markdown ("""<h1 style="font-family: 'Zen Dots', sans-serif; font-size: 60px;  text-align: center" >
                Stratify<span style="color:#1db954;">AI</span>
                </h1>
                <p style="font-family: 'Tektur', sans-serif; font-size: 26px; font-weight:500; text-align: center" >
                    Find <span style="color: #FB7185;">trending</span> topics. Generate smarter <span style="color: #3A75D2;">content ideas</span>
                </p>
             """, unsafe_allow_html=True
             )

#What do you want to analyze?
st.markdown ("""
             <br>
             <p style="font-family: tektur; font-size: 30px; text-align: center; font-weight: 600;" >
                What do you want to analyze?
             </p>
            """, unsafe_allow_html=True
)

#creation of background card for form
with st.container(border=True):

    mode = st.selectbox("Analysis Mode", ("Website URL", "Niche"), index=None, placeholder="Select what you want to analyze")

#URL Page
    if mode == "Website URL":
        url_input = st.text_input("Enter website URL to analyze", placeholder="https://example.com")
        url = url_input.strip()
        platform_radio = st.selectbox("Platform", ("Linkedin", "TikTok", "Instagram"), placeholder="Choose a platform", index=None)

        tone_radio = st.selectbox("Voice", ("Casual","Professional", "Funny"), index=None, placeholder="Choose a tone")
 
        days_slider = st.select_slider("Posts Planned", (3,4,5,6,7,8,9,10,11,14))

        generate_url = st.button("Generate Strategy", type = "primary", width="stretch")
        if generate_url:
            if url == "":
                st.warning("Please enter a URL")
            elif not url.startswith("http://") and not url.startswith("https://"):
                st.warning("You must enter a valid website starting with http:// or https://")
            elif platform_radio == None:
                st.warning("Please choose a platform.", )
            elif tone_radio == None:
                st.warning("Please choose a tone.")
            else:
                website = web_catcher(url)
                if website in url_error_messages:
                    st.error(website, icon="🚨")
                else:

                    with st.spinner ("Analyzing the website and generating content ideas...", show_time=True):
                        result_url = get_url_strategy(website, platform_radio, tone_radio, days_slider)
                        if result_url in gemini_errors_messages:
                            st.error(result_url, icon="🚨")
                        else:
                            st.session_state.generated_strategy = result_url
                            st.session_state.mode_result = "Website URL"
                            st.session_state.platform_result = platform_radio
                            st.session_state.voice_result = tone_radio
                            st.session_state.days_result = days_slider
        if (st.session_state.generated_strategy is not None and st.session_state.mode_result == mode):
            with st.container(border=True):
                st.header("Last Generated Strategy")
                col1, col2, col3 = st.columns(3)
                col1.metric("Platform", st.session_state.platform_result)
                col2.metric("Voice", st.session_state.voice_result)
                col3.metric("Posts Planned", st.session_state.days_result)
                st.markdown(st.session_state.generated_strategy)
                #Download strategy as text file
                st.download_button(label="Download Strategy", data=st.session_state.generated_strategy,
                                file_name="stratifyai_website_strategy.txt",
                                icon = ":material/download:")

#Niche Page
    elif mode == "Niche":
        niche_input = st.text_input("Enter Your Niche", placeholder="Example: fitness for college students")
        niche = niche_input.strip()

        platform_radio = st.selectbox("Platform", ("Linkedin", "TikTok", "Instagram"), placeholder="Choose a platform", index=None)

        tone_radio = st.selectbox("Voice", ("Casual","Professional", "Funny"), index=None, placeholder="Choose a tone")
 
        days_slider = st.select_slider("Posts Planned", (3,4,5,6,7,8,9,10,11,14))


#Generate strategy button
        generate_niche = st.button("Generate Strategy", type="primary", width="stretch")
        
        if generate_niche:
            if niche == "":
                st.warning("Please enter a niche.")
            elif platform_radio == None:
                st.warning("Please choose a platform.", )
            elif tone_radio == None:
                st.warning("Please choose a tone.")

            #Try-except to check if api rate limit reached or api failed. prints error message instead of showing error log
            else:
                topics = get_trending_topics(niche)
                if topics in niche_error_messages:
                    st.error(topics, icon="🚨")
                elif topics == []:
                    st.error("No trending topics found")
                else:
                    with st.spinner ("Finding niche trends and building your content strategy...", show_time=True):
                        result_niche = get_niche_strategy(topics, niche, platform_radio, tone_radio, days_slider)
                        if result_niche in gemini_errors_messages:
                            st.error(result_niche, icon="🚨")
                        else:
                            st.session_state.generated_strategy = result_niche
                            st.session_state.mode_result = "Niche"
                            st.session_state.platform_result = platform_radio
                            st.session_state.voice_result = tone_radio
                            st.session_state.days_result = days_slider
                            st.session_state.trend_headlines = topics
        if (st.session_state.generated_strategy is not None and st.session_state.mode_result == mode):
            with st.container(border=True):
                st.header("Last Generated Strategy")
                col1, col2, col3 = st.columns(3)
                col1.metric("Platform", st.session_state.platform_result)
                col2.metric("Voice", st.session_state.voice_result)
                col3.metric("Posts Planned",  st.session_state.days_result)
                with st.expander("Trend Sources"):
                    st.subheader("Relevant Headlines Found")
                    df = pd.DataFrame(st.session_state.trend_headlines, columns=["Relevant Headlines"])
                    st.table(df)
                st.divider()
                st.markdown(st.session_state.generated_strategy)
                #Download strategy as text file
                download_name = niche_input.lower().replace(" ", "_")
                st.download_button(label="Download Strategy", data=st.session_state.generated_strategy,
                                    file_name=f"stratifyai_{download_name}.txt",
                                    icon = ":material/download:")
    





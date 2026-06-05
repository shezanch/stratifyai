import streamlit as st

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
                Stratify<span style="color:#6FFF6F;">AI</span>
                </h1>
                <p style="font-family: 'Tektur', sans-serif; font-size: 26px; font-weight:500; text-align: center" >
                    Find <span style="color: #FB7185;">trending</span> topics. Generate smarter <span style="color: #3A75D2;">content ideas</span>
                </p>
             """, unsafe_allow_html=True
             )

#What do you want to analyze?
st.markdown ("""
             <p style="font-family: tektur; font-size: 30px; text-align: center; font-weight: 600;" >
                What do you want to analyze?
             </p>
            """, unsafe_allow_html=True
)

#creation of background card for form
with st.container(border=True):

    mode = st.selectbox("Select mode", ("URL", "Niche"), index=None, placeholder="Choose analysis mode")

#URL Page
    if mode == "URL":
        url_input = st.text_input("Enter website URL to analyze", placeholder="https://example.com")
        if url_input == "":
            st.warning("Please enter a URL")
        elif not url_input.startswith("http://") and not url_input.startswith("https://"):
            st.warning("You must enter a valid website starting with http:// or https://")
#Niche Page
    elif mode == "Niche":
        niche_input = st.text_input("Enter niche", placeholder="Example: fitness for college students")
        if niche_input == "":
            st.warning("Please enter a niche.")
        platform_radio = st.selectbox("Platform", ("Linkedin", "TikTok", "Instagram"), placeholder="Choose a platform", index=None)
        if platform_radio == None:
            st.warning("Please choose a platform.", )
        tone_radio = st.selectbox("Tone", ("Casual","Professional", "Funny"), index=None, placeholder="Choose a tone")
        if tone_radio == None:
            st.warning("Please choose a tone.")
        days_slider = st.select_slider("Days Of Content", (3,4,5,6,7,8,9,10,11,14))

#Niche user selection summary card
        with st.container(border=True):
            st.write("Content Settings")
            st.write("Niche: ", niche_input)
            st.write("Platform: ", platform_radio)
            st.write("Tone: ", tone_radio)
            st.write("Days of content: ", days_slider)
            st.write("")
        generate_niche = st.button("Generate Strategy", type="primary", width="stretch")




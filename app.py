import streamlit as st
import time

with st.sidebar:
    menu = st.markdown("#### MODE", text_alignment="left")
    platform_radio = st.selectbox("Platform", ("Linkedin", "TikTok", "Instagram"), placeholder="Choose an option", accept_new_options=False)
    tone_radio = st.selectbox("Tone", ("Casual","Professional", "Funny"))
    days_slider = st.select_slider("Days Of Content", (3,4,5,6,7,8,9,10,11,14))
    st.write("You selected: ", platform_radio)
st.markdown ("# Stratify:green[AI]", width ="stretch", text_alignment="center")
st.markdown("### Find :red[trending] topics. Generate smarter :blue[content ideas]", text_alignment="center", width="stretch")

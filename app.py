import os

import streamlit as st
from dotenv import load_dotenv

from apputil import Genius

# load ACCESS_TOKEN from the .env file
load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


st.write(
'''# Week 6: Genius API''')

# stop early if the token is missing
if not ACCESS_TOKEN:
    st.error("No ACCESS_TOKEN found. Add it to your .env file.")
    st.stop()

genius = Genius(access_token=ACCESS_TOKEN)


# Exercise 2: look up a single artist
st.write("## Single Artist")

search_term = st.text_input("Artist name:", value="Radiohead")

if st.button("Get Artist") and search_term:
    artist = genius.get_artist(search_term).get("response", {}).get("artist")

    if artist:
        # show the artist's picture next to a few basic stats
        col1, col2 = st.columns([1, 2])
        col1.image(artist.get("image_url"))
        col2.write(f"### {artist.get('name')}")
        col2.write(f"**Artist ID:** {artist.get('id')}")
        col2.write(f"**Followers:** {artist.get('followers_count')}")
        col2.write(f"[View on Genius]({artist.get('url')})")

        # full JSON response
        with st.expander("Raw JSON"):
            st.json(artist)
    else:
        st.warning(f"No artist found for '{search_term}'.")


# Exercise 3: look up several artists at once
st.write("## Multiple Artists")

terms_text = st.text_area("Artist names (one per line):",
                          value="Rihanna\nTycho\nSeal\nU2")

if st.button("Get Artists"):
    # turn the text box into a list, skipping blank lines
    search_terms = [t.strip() for t in terms_text.splitlines() if t.strip()]

    if search_terms:
        with st.spinner("Searching Genius..."):
            df = genius.get_artists(search_terms)
        st.dataframe(df, hide_index=True)
    else:
        st.warning("Enter at least one artist name.")

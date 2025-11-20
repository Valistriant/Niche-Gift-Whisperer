import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# 1. Get your key here: https://aistudio.google.com/app/apikey
# 2. Once you have your Amazon Associates ID, paste it below.
AMAZON_TAG = "YOUR_TAG_HERE-20" 

st.set_page_config(page_title="Gift Whisperer", page_icon="🎁")

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.header("⚙️ Setup")
    api_key = st.text_input("Enter Google API Key", type="password")
    st.info("Get your free API key from Google AI Studio.")

# --- MAIN APP ---
st.title("🎁 The Niche Gift Whisperer")
st.markdown("Tell me about the person, and I'll find the perfect gifts.")

# User Input
user_input = st.text_area(
    "Describe the recipient:", 
    placeholder="e.g., My 34-year-old brother who loves retro gaming, dark roast espresso, and 90s hip hop..."
)

if st.button("Find Gift Ideas"):
    if not api_key:
        st.error("Please enter your Google API Key in the sidebar to start.")
    elif not user_input:
        st.warning("Please describe the person first!")
    else:
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # The Strategy: Ask for a strict format (Pipe separated) to make coding easy
        prompt = f"""
        Suggest 5 specific, physical products available on Amazon for this person: '{user_input}'.
        Return ONLY the product names separated by a pipe symbol (|). 
        Do not include numbering or descriptions.
        Example format: Product A | Product B | Product C
        """

        with st.spinner("Consulting the gift spirits..."):
            try:
                response = model.generate_content(prompt)
                # Split the response into a list
                gift_ideas = response.text.split('|')

                st.success("Here are 5 ideas. Click to view on Amazon:")
                
                # Display results
                for idea in gift_ideas:
                    idea = idea.strip()
                    if idea: # check if not empty
                        # Create the Amazon Affiliate Search Link
                        # Logic: amazon.com/s?k=[Search Term]&tag=[Your ID]
                        search_term = idea.replace(" ", "+")
                        link = f"https://www.amazon.com/s?k={search_term}&tag={AMAZON_TAG}"
                        
                        # Display as a clear card
                        with st.container(border=True):
                            col1, col2 = st.columns([3, 1])
                            col1.subheader(idea)
                            col2.link_button("Check Price ↗", link)
                            
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Note: As an Amazon Associate, I earn from qualifying purchases.")
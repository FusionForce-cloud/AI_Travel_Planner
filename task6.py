import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from googletrans import Translator
from dotenv import load_dotenv
import os

# ✅ Load API Key securely from .env or Streamlit Secrets
load_dotenv()
GOOGLE_API_KEY = os.getenv("Your_google_API")  # Secure API Key Handling

# ✅ Streamlit Page Configuration
st.set_page_config(page_title="AI Travel Assistant", layout="wide")

# ✅ Title
st.markdown("<h1 style='text-align:center;'>🗺️✈︎ Destination Dynamo AI</h1>", unsafe_allow_html=True)

# ✅ User Input Form
col1, col2 = st.columns(2)

with col1:
    source_city = st.text_input("🛫 Departure City", placeholder="E.g., New Delhi")
    destination_city = st.text_input("📍 Destination City", placeholder="E.g., Amsterdam")
    travel_date = st.date_input("📆 Travel Date")
    currency = st.selectbox("💲 Currency", ["USD", "INR", "EUR", "GBP", "JPY"])

with col2:
    preferred_mode = st.selectbox("🚗 Preferred Mode", ["Any", "Flight", "Train", "Bus", "Cab"])
    sort_by = st.radio("📊 Sort By", ["Price", "Duration"])
    language = st.selectbox("🌍 Select Language", ["English", "Spanish", "French", "German", "Hindi"])

# ✅ Language Code Mapping for Translation
language_codes = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
}

# ✅ Function to fetch AI-generated travel options
def get_travel_options(source, destination, mode, currency):
    system_prompt = SystemMessage(
        content="You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with estimated costs, duration, and relevant travel tips."
    )
    user_prompt = HumanMessage(
        content=f"I am traveling from {source} to {destination} in {currency}. Preferred mode: {mode}. Suggest travel options with estimated cost, duration, and important details."
    )

    # ✅ Initialize AI model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"

# ✅ Function to Translate Text
def translate_text(text, target_language):
    if target_language == "English":  # No translation needed
        return text

    translator = Translator()
    translated_text = translator.translate(text, dest=language_codes.get(target_language, "en")).text
    return translated_text

# ✅ Button to Fetch Travel Options
if st.button("🔍 Find Travel Options"):
    if source_city.strip() and destination_city.strip():
        with st.spinner("🔄 Fetching best travel options..."):
            travel_info = get_travel_options(source_city, destination_city, preferred_mode, currency)

        # Translate if necessary
        translated_info = translate_text(travel_info, language)

        # Display Results
        st.success("✅ AI-Generated Travel Recommendations:")
        st.markdown(translated_info)
    else:
        st.warning("⚠️ Please enter both source and destination locations.")

# ✅ Footer
st.markdown(
    """
    <div style='text-align:center; padding:10px; margin-top:20px; font-weight:bold;'>
        Created by Sai Kamal 🚀
    </div>
    """,
    unsafe_allow_html=True
)

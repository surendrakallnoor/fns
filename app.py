import streamlit as st
import plotly.express as px
import requests
from bs4 import BeautifulSoup

st.title("FinSmart — Your AI Wealth Manager")

st.sidebar.header("Investor Profile")

name = st.sidebar.text_input("Enter your name")
age = st.sidebar.number_input("Enter your age", 18, 80)

st.header("Risk Profiling Quiz")

q1 = st.selectbox("If your investment drops 20%, what will you do?",
                  ["Sell immediately", "Hold", "Buy more"])

q2 = st.selectbox("Investment duration?",
                  ["< 1 year", "1-3 years", "5+ years"])

score = 0

if q1 == "Sell immediately":
    score += 1
elif q1 == "Hold":
    score += 2
else:
    score += 3

if q2 == "< 1 year":
    score += 1
elif q2 == "1-3 years":
    score += 2
else:
    score += 3

if st.button("Calculate Risk Profile"):
    
    if score <= 2:
        risk = "Safe Investor"
        data = [20, 60, 20]
    elif score <= 4:
        risk = "Balanced Investor"
        data = [50, 30, 20]
    else:
        risk = "Aggressive Investor"
        data = [80, 10, 10]

    st.success(f"Your Risk Profile: {risk}")

    fig = px.pie(
        names=["Equity", "Debt", "Gold"],
        values=data,
        title="Recommended Portfolio"
    )

    st.plotly_chart(fig)
st.header("Market News & Sentiment")
url = "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

items = soup.find_all("item")[:5]

for item in items:
    headline = item.title.text.lower()

    if any(word in headline for word in ["rally", "surge", "gain", "rise"]):
        sentiment = "🟢 Bullish"
    elif any(word in headline for word in ["fall", "crash", "loss", "drop"]):
        sentiment = "🔴 Bearish"
    else:
        sentiment = "🟡 Neutral"

    st.write(f"{item.title.text} — {sentiment}")
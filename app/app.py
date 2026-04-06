import streamlit as st
import joblib
import pandas as pd

# Load model
model = joblib.load("model/delay_model.pkl")

# Page config
st.set_page_config(page_title="Smart Transport AI", layout="wide")

# ----------- DARK THEME CSS -----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}
h1, h2, h3 {
    color: #38bdf8;
}
.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}
button[kind="primary"] {
    background-color: #38bdf8;
    color: black;
}
</style>
""", unsafe_allow_html=True)

# ----------- NAVBAR -----------
menu = st.radio("", ["🏠 Home", "📊 Dashboard", "🚀 Predict", "🔐 Admin"], horizontal=True)

# ================= HOME =================
if menu == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>🚍 Smart Transport AI</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>✨ Welcome</h3>
    <p>This AI system predicts transport delays using real-time conditions like traffic, weather and time.</p>
    </div>
    """, unsafe_allow_html=True)

    st.image("https://images.unsplash.com/photo-1494515843206-f3117d3f51b7", use_container_width=True)

# ================= DASHBOARD =================
elif menu == "📊 Dashboard":
    st.markdown("## 📊 Live Dashboard")

    df = pd.read_csv("../data/data.csv")

    df['delay'] = (
        pd.to_datetime(df['actual_time'], format='%H:%M') -
        pd.to_datetime(df['scheduled_time'], format='%H:%M')
    ).dt.total_seconds()/60

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Delay", f"{df['delay'].mean():.2f} min")
    col2.metric("Max Delay", f"{df['delay'].max():.2f} min")
    col3.metric("Min Delay", f"{df['delay'].min():.2f} min")

    st.line_chart(df['delay'])

# ================= PREDICT =================
elif menu == "🚀 Predict":
    st.markdown("## 🚀 Predict Delay")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        traffic = st.slider("Traffic 🚦", 1, 10, 5)

    with col2:
        weather = st.selectbox("Weather 🌦", ["Clear", "Cloudy", "Rain"])

    with col3:
        hour = st.slider("Hour ⏰", 0, 23, 9)

    if st.button("🔮 Predict Now"):
        weather_map = {'Clear':0, 'Cloudy':1, 'Rain':2}

        data = pd.DataFrame([[traffic, weather_map[weather], hour]],
                            columns=['traffic_level', 'weather', 'hour'])

        prediction = model.predict(data)[0]

        st.markdown(f"""
        <div class="card">
        <h2>🚍 Delay: {prediction:.2f} minutes</h2>
        </div>
        """, unsafe_allow_html=True)

        if prediction > 10:
            st.error("⚠️ High Delay Expected!")
        else:
            st.success("✅ Delay Normal")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= ADMIN =================
elif menu == "🔐 Admin":
    st.markdown("## 🔐 Admin Panel")

    pwd = st.text_input("Enter Password", type="password")

    if pwd == "admin123":
        st.success("Access Granted")

        df = pd.read_csv("../data/data.csv")
        st.dataframe(df)

    else:
        st.warning("Enter correct password")
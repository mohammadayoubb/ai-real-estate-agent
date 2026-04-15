import streamlit as st
import requests

st.set_page_config(page_title="AI Real Estate Predictor", layout="centered")

st.title("🏠 AI Real Estate Price Predictor")

st.write("Enter a house description and get an AI-powered price prediction.")

# Input box
user_input = st.text_area("House Description", height=150)

# Button
if st.button("Predict Price"):

    if not user_input.strip():
        st.warning("Please enter a description.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"query": user_input}
            )

            data = response.json()

            if data["status"] == "success":

                st.success("Prediction Successful!")

                # Price
                price = data["prediction"]["predicted_price"]
                st.subheader(f"💰 Predicted Price: ${price:,.2f}")

                # Features
                with st.expander("📊 Extracted Features"):
                    st.json(data["features"])

                # Interpretation
                st.subheader("🧠 Explanation")
                st.write(data["interpretation"]["interpretation"])

            else:
                st.error("Something went wrong.")
                st.json(data)

        except Exception as e:
            st.error(f"Error: {str(e)}")
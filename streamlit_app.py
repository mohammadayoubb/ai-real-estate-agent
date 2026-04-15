import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI Real Estate Price Predictor",
    page_icon="🏠",
    layout="centered"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-text {
        color: #666;
        margin-bottom: 1.5rem;
    }
    .price-card {
        background-color: #f3f8ff;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #dbeafe;
        text-align: center;
        margin: 15px 0;
    }
    .price-label {
        font-size: 1rem;
        color: #555;
    }
    .price-value {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
    }
    .section-box {
        background-color: #fafafa;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-top: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏠 AI Real Estate Price Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">Describe a property in natural language and get extracted features, a predicted price, and an AI explanation.</div>',
    unsafe_allow_html=True
)

with st.expander("Example input"):
    st.code(
        "A well-maintained 2-story family home with 2800 square feet of living space, "
        "4 bedrooms, 3 full bathrooms, and a total of 9 rooms. The house has an overall "
        "quality rating of 8, includes a 2-car garage, and sits on a 9500 square foot lot. "
        "It was built in 2015 and is located in the desirable NridgHt neighborhood."
    )

user_input = st.text_area(
    "House Description",
    height=180,
    placeholder="Enter a house description here..."
)

col1, col2 = st.columns([1, 1])
with col1:
    predict_clicked = st.button("Predict Price", use_container_width=True)
with col2:
    clear_clicked = st.button("Clear", use_container_width=True)

if clear_clicked:
    st.rerun()

if predict_clicked:
    if not user_input.strip():
        st.warning("Please enter a house description first.")
    else:
        with st.spinner("Analyzing property and generating prediction..."):
            try:
                response = requests.post(
                    "https://ai-real-estate-agent-937b.onrender.com/predict",
                    json={"query": user_input},
                    timeout=60
                )

                data = response.json()

                if data.get("status") == "success":
                    price = data["prediction"]["predicted_price"]
                    features = data["features"]
                    interpretation = data["interpretation"]["interpretation"]

                    st.success("Prediction completed successfully.")

                    st.markdown(f"""
                        <div class="price-card">
                            <div class="price-label">Predicted Price</div>
                            <div class="price-value">${price:,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.subheader("AI Explanation")
                    st.markdown(f'<div class="section-box">{interpretation}</div>', unsafe_allow_html=True)

                    st.subheader("Extracted Features")
                    display_features = {
                        "Living Area (sq ft)": features.get("gr_liv_area"),
                        "Bedrooms": features.get("bedroom_abvgr"),
                        "Full Bathrooms": features.get("full_bath"),
                        "Neighborhood": features.get("neighborhood"),
                        "Overall Quality": features.get("overall_qual"),
                        "Garage Capacity": features.get("garage_cars"),
                        "Year Built": features.get("year_built"),
                        "Lot Area": features.get("lot_area"),
                        "House Style": features.get("house_style"),
                        "Total Rooms": features.get("totrms_abvgrd"),
                    }
                    st.json(display_features)

                elif data.get("status") == "incomplete":
                    st.warning("The description is missing some required details.")
                    st.write("Missing fields:")
                    st.write(data.get("missing_fields", []))

                    if "features" in data:
                        st.subheader("Extracted Features So Far")
                        st.json(data["features"])

                else:
                    st.error("The request could not be completed.")
                    st.json(data)

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI backend. Make sure the API server or Docker container is running.")
            except requests.exceptions.Timeout:
                st.error("The request took too long. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
[README.md](https://github.com/user-attachments/files/26854132/README.md)
 # AI Real Estate Agent

An AI-powered system that converts natural language property
descriptions into structured features, predicts property prices using a
trained machine learning model, and provides human-readable
explanations.


# Project Overview

This project simulates an intelligent real estate assistant. Users can
describe a property in plain English, and the system will:

1.  Extract structured features using an LLM
2.  Predict the property price using a trained ML model
3.  Generate a natural language explanation of the prediction


# System Architecture

Pipeline flow:

User Input → LLM Feature Extraction → Validation → Prediction →
Explanation → API Response


# Project Structure

-   main.py → FastAPI entry point and endpoints
-   llm_chain.py → LLM feature extraction
-   predictor.py → ML prediction
-   interpreter.py → Explanation generation
-   prompts.py → Stage 1 & Stage 2 prompts
-   schemas.py → Data validation
-   model/ → Saved ML model
-   Dockerfile → Deployment


#  Technologies Used

-   FastAPI
-   OpenAI API
-   Scikit-learn
-   Pydantic
-   Docker
-   Render


#  Key Features

-   Natural language → structured data
-   AI-based feature extraction
-   ML price prediction
-   Explanation generation


# How It Works

1.  User inputs property description
2.  LLM extracts structured features
3.  Model predicts price
4.  System explains prediction


# API Endpoint

POST /predict

Example request: { "query": "A modern 4-bedroom house with a garage" }


#  Docker

Build: docker build -t ai-real-estate-agent .

Run: docker run -p 8000:8000 ai-real-estate-agent


# Render

used render for hosting


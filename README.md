# Personalized Marketing Copy AI

## Overview
Personalized Marketing Copy AI is a full-stack web application that converts customer profile data into polished marketing emails. It collects information such as the customer’s name, age, gender, location, purchase history, favorite category, and total spending. The app then analyzes that data to determine the customer segment, loyalty level, spending range, and the best discount suggestion. Using a local open-source language model, it generates a tailored subject line and email body without requiring any API keys or paid services.

## Why This Project Exists
This project demonstrates how AI can be used in practical marketing workflows. It combines data analysis, prompt building, and content generation into a simple experience that can be run locally. It is useful for small businesses, marketing teams, and developers who want to explore AI-generated copy without depending on external SaaS platforms.

## Core Features
- Collects customer demographics and purchase behavior
- Classifies users into segments such as New, Regular, Premium, and VIP
- Recommends products based on browsing and spending patterns
- Generates personalized email content with a matching subject line
- Supports multiple tone options including Friendly, Luxury, Urgent, and Promotional
- Provides validation and cleaning for AI-generated output
- Runs locally with Flask and an open-source model

## Tech Stack
- Frontend: HTML, CSS, and JavaScript
- Backend: Python and Flask
- AI Layer: Hugging Face Transformers and PyTorch
- Deployment: Render-ready with a simple single-service setup

## Project Structure
- backend/: Flask application, routes, services, prompts, and model logic
- frontend/: Static UI files served by the backend
- docs/: Architecture, API, and deployment documentation
- render.yaml: Deployment configuration for hosting

## Setup
1. Create a Python virtual environment.
2. Install the dependencies from backend/requirements.txt.
3. Run the Flask application from the backend directory.
4. Open the app in your browser and start generating emails.

## How It Works
The user fills in the form with customer information. The backend validates the input, analyzes the profile, and builds a structured prompt. That prompt is sent to the local AI model, which returns a subject and email body. The response is then cleaned and returned to the frontend for display.

## Use Cases
- Personalized promotional campaigns
- Customer retention email generation
- E-commerce marketing automation
- AI experimentation for copywriting workflows

## Notes
This repository is intentionally simple and beginner-friendly. It focuses on clarity, modularity, and practical use rather than over-engineering. The goal is to provide a workable example of AI-assisted marketing content generation that anyone can explore and extend.

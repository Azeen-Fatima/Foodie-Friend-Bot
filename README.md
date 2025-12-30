# Foodie Friend - AI Restaurant Chatbot

**Foodie Friend** is an AI-powered conversational agent developed for **Crave Lounge**, a restaurant based in Gujranwala, Pakistan. The chatbot assists customers in exploring the menu, checking prices, and placing food orders through an interactive interface.



##  Live Demo

You can interact with the live bot here: [https://foodie-chatbot-iroy.onrender.com](https://foodie-chatbot-iroy.onrender.com)



##  Features

- **AI-Powered Conversations:** Uses the Google Gemini AI model to provide natural, human-like responses to customer queries.  
- **Menu Exploration:** Customers can browse specific categories (Fast Food, Chinese, Desi, etc.) or view the full menu.  
- **Automated Ordering System:** Collects user details (Name, Phone, and Address) and calculates the total bill including a flat delivery fee (Rs. 200).  
- **Receipt Generation:** Provides a detailed order summary and estimated delivery time (40-50 minutes) upon confirmation.  
- **Order Locking:** Once an order is confirmed, the system prevents adding new items to maintain order integrity.  
- **Multilingual Support:** Capable of interacting in multiple languages for a localized experience.  
- **Smart Fallbacks:** Politely handles unrelated queries and guides users back to the restaurant menu.  



##  Tech Stack

- **Backend:** Python (Flask)  
- **Frontend:** HTML, CSS, JavaScript  
- **AI Model:** Google Gemini API  
- **Server:** Gunicorn  
- **Deployment:** Render  



## 📂 Project Structure

```text
project-chatbot/
├── app.py              # Flask backend logic and AI integration
├── requirements.txt    # List of dependencies
├── Procfile            # Deployment instructions for Render
└── templates/
    └── index.html      # Frontend UI (including CSS & JS)

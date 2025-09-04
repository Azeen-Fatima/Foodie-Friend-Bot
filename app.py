from flask import Flask, request, jsonify, render_template, session
import google.generativeai as genai
import os
import re

# API Key Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Restaurant Data & Bot Instructions
restaurant_menu = {
    "Chinese": {
        "Chicken Manchurian": {"price": "Rs. 750"},
        "Chicken Chilli Dry": {"price": "Rs. 800"},
        "Spaghetti": {"price": "Rs. 650"},
        "Chicken Mongolian": {"price": "Rs. 850"},
        "Fried Egg Rice": {"price": "Rs. 550"}
    },
    "Fast Food": {
        "Zinger Burger": {"price": "Rs. 450"},
        "Chicken Shawarma": {"price": "Rs. 300"},
        "Loaded Fries": {"price": "Rs. 400"},
        "Club Sandwich": {"price": "Rs. 500"},
        "Pizza": {
            "Chicken Fajita": {
                "Small": "Rs. 850",
                "Medium": "Rs. 1350",
                "Large": "Rs. 1850"
            },
            "Pepperoni": {
                "Small": "Rs. 900",
                "Medium": "Rs. 1400",
                "Large": "Rs. 1900"
            },
            "Veggie Delight": {
                "Small": "Rs. 800",
                "Medium": "Rs. 1300",
                "Large": "Rs. 1800"
            }
        }
    },
    "Desi Food": {
        "Chicken Biryani": {"price": "Rs. 450"},
        "Mutton Karahi": {"price": "Rs. 1800"},
        "Beef Pulao": {"price": "Rs. 700"},
        "Dal Mash": {"price": "Rs. 300"},
        "Chicken Seekh Kebab": {"price": "Rs. 600"}
    },
    "Beverages": {
        "Cold Drink": {"price": "Rs. 120"},
        "Lassi": {"price": "Rs. 150"},
        "Fresh Lime Soda": {"price": "Rs. 200"},
        "Mint Margarita": {"price": "Rs. 250"},
        "Tea": {"price": "Rs. 100"}
    }
}

system_prompt = f"""
You are a friendly and helpful food bot, created by Azeen Fatima and Iqra Azam, named "Foodie Friend" for a Pakistani restaurant named "Crave Lounge". 
Your primary purpose is to assist customers with their food orders, answer questions about the menu, 
and provide information on prices.

### Menu
{restaurant_menu}

### Restaurant Information
- *Location:* Model Town, Gujranwala
- *Delivery Area:* Only within Gujranwala
- *Delivery Charges:* Rs. 200 (flat rate)
- *Delivery Time:* 40-50 minutes max

### Instructions for You:
1. *Menu & Prices:* When a user asks about the menu, show them a only catagories and ask them which catagories menu they want to see also ask them wether they want to see full menu, show the menu of catagory name the user select. If user ask to see full menu show them a categorized list of full menu. When they ask for a price, provide the exact amount from the menu in PKR.
2. *Delivery & Charges:* Politely confirm the delivery charges and the area.
3. *Ordering Flow:* If a user wants to order, start by asking for their name, then their phone number, and finally their address. 
   Only after all three details are provided should you confirm the order.
4. *Receipt:* Once details are collected, show a message including name, phone, address, items, delivery charges (200), and total. 
   Ask the user to confirm with "yes" or "no".
5. *After Confirmation:* If the order is confirmed, mark it as placed. 
   Do not allow adding new items to this order. If the user asks to add, politely say that a new order must be placed.
6. *Address Confirmation:* If a user only provides "Gujranwala", ask them to provide an exact area.
7. *Phone Validation:* Ensure the phone number is in Pakistani format. If not, ask them again.
8. *Delivery Time:* When confirming an order, state the delivery time as 40-50 minutes.
9. *Out-of-Topic Questions:* If a user asks a question not related to food or the restaurant, answer politely and then guide them back by asking: "Is there anything I can help you with from our delicious menu?"
10. *Natural Language:* Respond in a conversational, polite, and natural tone.
"""

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key_here'

@app.route("/")
def index():
    session['history'] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    try:
        model = genai.GenerativeModel(
            model_name="gemma-3-12b-it"
        )

        history_from_session = session.get('history', [])

        history_for_api = []
        if not history_from_session:
            history_for_api.append({'role': 'user', 'parts': [{'text': system_prompt}]})
            history_for_api.append({'role': 'model', 'parts': [{'text': "👋 Welcome to Crave Lounge! i am your Foodie Friend. How can I help you today?"}]})
        else:
            history_for_api = history_from_session

        chat_session = model.start_chat(history=history_for_api)

        response = chat_session.send_message(user_message)

        new_history = [{'role': m.role, 'parts': [{'text': p.text} for p in m.parts]} for m in chat_session.history]
        session['history'] = new_history

        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Sorry, a server error occurred. Please try again."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




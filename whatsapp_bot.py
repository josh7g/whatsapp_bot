from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

class RenmoChatbot:
    def __init__(self):
        self.intents = {
            "greeting": ["hi", "hello", "hey", "good day", "good morning", "good evening"],
            "about": ["tell me about renmo", "what is renmo", "about renmo"],
            "how_it_works": ["how does it work", "explain the process", "how can I apply", "steps to apply"],
            "benefits": ["why should I choose renmo", "benefits of renmo", "advantages", "why renmo"],
            "corporate_partnership": ["corporate partnership", "partner with renmo", "organization partnership"],
            "testimonials": ["feedback", "reviews", "what are people saying", "testimonials"],
            "faq": ["questions", "faq", "common questions"],
            "for_landlords": ["landlord", "agent", "property owner", "collaborate"],
            "start_application": ["apply", "start application", "how to apply"],
            "properties": ["show properties", "show houses", "available properties", "available houses","home"]
        }

        self.responses = {
            "greeting": "Hello! Welcome to Renmo Homes. How can I assist you today?",
            "about": "Renmo is the No.1 platform in Ghana that allows tenants to pay MONTHLY rent for their homes. We believe everyone deserves a decent home without the stress of bulk advance payments.",
            "how_it_works": "It's a simple process: 1) Application - Submit your details and property particulars. 2) Verification - Get your documents and property approved. 3) Move In - Once approved, Renmo will make payment to your landlord and you can settle in your new home.",
            "benefits": "Choosing Renmo allows you to save money for emergencies, access financial support without going to a bank, find your own house or look for houses on our website, enjoy flexible options regardless of property type, earn loyalty points for discounts on your next rent, pay rent monthly, and experience no hidden fees.",
            "corporate_partnership": "RenMo partners with organizations to provide home rental services to employees. Services include Rent & Pay Monthly, Home Searches, and Rent-To-Own options.",
            "testimonials": "Our clients love us! For instance, Kofi A. mentioned, 'It was a very smooth experience with RenMo. I didn't even have to come to their office during the whole process.'",
            "faq": "Some FAQs include: Do I need to be a full-time employee to access Renmo's services? Answer: No, just proof of regular income. Does Renmo take collateral from the tenant? Answer: No. Can I find my own properties and request funding from Renmo? Answer: Yes.",
            "for_landlords": "If you're a landlord or agent, Renmo can help you find the right tenant. We ensure that renting out your property is smooth and beneficial.",
            "start_application": "You can start your application by visiting the Renmo website or using our unique USSD code.",
            "properties": [
                ("Two Bedroom Apartment @ Ablekuma for Ghc2,498 Monthly. Features include two bedrooms with two washrooms each, fitted kitchen, spacious living room, and more.", "https://renmoproperties.files.wordpress.com/2023/09/property1.jpg"),
                # will add more properties soon
            ]
        }

    def get_response(self, message):
        message = message.lower()
        for intent, keywords in self.intents.items():
            for keyword in keywords: 
                if keyword in message:
                    return self.responses[intent]
        return "Sorry, I didn't understand that. Can you please rephrase or ask another question?"

app = Flask(__name__)
chatbot = RenmoChatbot()

@app.route("/webhook", methods=["GET", "POST"])
def whatsapp_reply():
    user_message = request.values.get('Body', '').lower()
    bot_response = chatbot.get_response(user_message)
    twilio_response = MessagingResponse()
    msg = twilio_response.message()
    
    if user_message in chatbot.intents["properties"]:
        for property_info, image_url in bot_response:
            msg.body(property_info)
            msg.media(image_url)
    else:
        msg.body(bot_response)

    # Debugging: Print request details
    print("Received WhatsApp message:")
    print(f"Body: {request.values.get('Body', '')}")
    print(f"From: {request.values.get('From', '')}")
    print(f"To: {request.values.get('To', '')}")
    
    return str(twilio_response)


@app.route("/")
def home():
    return "Welcome to the Renmo Chatbot!"

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # Set the port explicitly to 8080
#set the port to 8080 because twillo was having difficulty in accessing localhost:5000
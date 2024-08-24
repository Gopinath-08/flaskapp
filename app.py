from flask import Flask, request, jsonify, render_template
import datetime
import random
import requests
import webbrowser

app = Flask(__name__)

def get_current_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."

def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why don't some couples go to the gym? Because some relationships don't work out!"
    ]
    return random.choice(jokes)

def tell_hello():
    greetings = [
        "Hello! How can I assist you today?",
        "Hi there! What can I do for you?",
        "Hey! How can I help you today?",
        "Good morning! How can I help you?",
        "Good afternoon! What can I do for you?",
        "Good evening! How can I assist you today?"
    ]
    return random.choice(greetings)

def fetch_weather(city):
    # Placeholder for real weather API integration
    return f"The weather in {city} is sunny with a chance of rain."

def fetch_news():
    api_key = '58ed14d6d9a841f39260b342e99e8ce3'  # Replace with your actual API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("articles"):
            articles = data["articles"][:5]
            headlines = [article["title"] for article in articles]
            return "Here are the top headlines: " + ", ".join(headlines)
        else:
            return "I couldn't retrieve the news."
    except Exception as e:
        return "There was an error retrieving the news."

def open_application(app_name):
    apps = {
        "browser": "http://www.google.com",
        "notepad": "notepad.exe",
        "calculator": "calc.exe"
    }
    url = apps.get(app_name.lower())
    if url:
        webbrowser.open(url)
        return f"Opening {app_name}."
    else:
        return "I don't know how to open that application."

def simple_ai_model(input_data):
    input_data = input_data.lower()

    if "time" in input_data:
        return get_current_time()
    elif "joke" in input_data:
        return tell_joke()
    elif "hello" in input_data:
        return tell_hello()
    elif "weather" in input_data:
        city = input_data.split("in")[-1].strip()
        return fetch_weather(city)
    elif "news" in input_data:
        return fetch_news()
    elif "open" in input_data:
        app_name = input_data.split("open")[-1].strip()
        return open_application(app_name)
    else:
        return "I'm not sure how to help with that. Can you ask something else?"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        user_input = data.get('input')
        first_interaction = data.get('firstInteraction', False)

        if first_interaction:
            greeting = "Hello! I am your virtual assistant. How can I assist you today?"
            return jsonify({'response': greeting})

        response = simple_ai_model(user_input)
        return jsonify({'response': response})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

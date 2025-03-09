from datetime import datetime
from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
API_KEY = "3f03559aebf15cc0ff68b1fef6d7d588"
weather_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global weather_history
    error = None
    weather_data = None
    
    if request.method == 'POST':
        city = request.form.get('city').strip()
        
        if not city:
            error = 'Введите название города'
        else:
            try:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    weather_data = {
                        'city': data['name'],
                        'temp': round(data['main']['temp'] - 273.15, 1),
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'description': data['weather'][0]['description'].capitalize(),
                        'time': datetime.now().strftime('%H:%M %d.%m.%Y')
                    }
                    weather_history.insert(0, weather_data)
                    
                    if len(weather_history) > 10:
                        weather_history.pop()
                        
                else:
                    error = 'Город не найден'
            except Exception as e:
                error = f'Ошибка получения данных: {str(e)}'

    return render_template('index.html',
                         weather=weather_data,
                         error=error,
                         history=weather_history)

def print_startup_message():
    print("\n----------------------------------------")
    print("  Сервис погоды запущен!")
    print(f"  Доступен по адресу: http://localhost:5000")
    print("----------------------------------------\n")

if __name__ == '__main__':
    print_startup_message()
    app.run(debug=True)
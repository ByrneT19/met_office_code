import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
# Determine that the user has entered a valid city
## Work out how to include spaces, i.e New York, etc don't work
def city_check():
    user_input = input('Please type in the name of a city. ').lower()
    check = True
    while check:
        if user_input == '' or not(user_input.isalpha()):
            print('Please enter a valid city name.')
            user_input = input('Please type in the name of a city. ')
        else:
            check = False
    return user_input

def api_call():
    city = city_check()
    # https to protect passwords, tokens, or personal data being intercepted
    url = 'https://durvp011gk.execute-api.eu-west-1.amazonaws.com/v1/api/forecasts?city=%s' % city 
    # Try block for GET request
    try:
        response = requests.get(
            url, 
            headers = {
                # API key held in .env file
                'x-api-key': os.getenv("API_KEY"),
                'Accept': 'application/json'
            })
    except requests.exceptions.ConnectionError:
        print('Connection failed - please check the URL or try again later')
    # Check response is the expected JSON response and not something else
    if response.headers.get('Content-Type').startswith('application/json'):
        # Returns a dictionary of the JSON response
        data = response.json()
    else:
        print('Unexpected non-JSON response')
    # Variable for un-recorded data
    no_recorded_value = 'null'
    # Loop through the returned data
    for item in data['features'][0]['properties']['timeSeries']:
        # Assign values for terminal output
        if 'screenTemperature' in item:
            screen_temp = item['screenTemperature']
        else:
            screen_temp = no_recorded_value
        if 'time' in item:
            # Return the date in a simplified format
            date_figure = item['time'].split('T')[0]
            time = item['time'].split('T')[1][:-1]
        else:
            time = no_recorded_value
        if 'maxScreenAirTemp' in item:
            max_temp = item['maxScreenAirTemp']
        else:
            max_temp = no_recorded_value
        if 'minScreenAirTemp' in item:
            min_temp = item['minScreenAirTemp']
        else:
            min_temp = no_recorded_value

        # Logical operators to print out the results of the API call using the above variables
        # Result for date with both values
        if max_temp != no_recorded_value and min_temp != no_recorded_value:
            print(f'On {date_figure} at {time} the max temp was: {max_temp}, and the min temp was: {min_temp}')
        # Result for max_temp only (with and without screen_temp)
        if max_temp != no_recorded_value and min_temp == no_recorded_value:
            if screen_temp != no_recorded_value:
                print(f'On {time} the max temp was: {max_temp}, and the screen temp was: {screen_temp}')
            else:
                print(f'On {time} the max temp was: {max_temp}')
        # Result for min_temp only (with and without screen_temp)
        if max_temp == no_recorded_value and min_temp != no_recorded_value:
            if screen_temp != no_recorded_value:
                print(f'On {time} the screen temp was: {screen_temp}, and the min temp was: {min_temp}')
            else:
                print(f'On {time} the min temp was: {min_temp}')
        # Result for screen_temp only
        if max_temp == no_recorded_value and min_temp == no_recorded_value:
            if screen_temp != no_recorded_value:
                print(f'On {time} the screen temp was: {screen_temp}')
            else:
                # Result for no data in any of the three categories
                print(f'On {time} no data was recorded.') 

        # Create a dictionary of the returned data to turn into JSON
        response_data = {
            'time' : time,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'screenTemp': screen_temp
        }
        # Create JSON data from the received data
        local_JSON_data = json.dumps(response_data)
        # Append each line of the looped data into a .txt file and save it locally in the pwd
        file = open('weather_data.txt', 'a+') 
        file.write(local_JSON_data)
        file.write('\n')
    file.close()


if __name__ == "__main__":
    api_call()
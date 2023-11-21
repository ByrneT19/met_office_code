# met_office_code

## An API call exercise to obtain weather data from AWS and create a local JSON file
This programme executes an API GET request to an AWS server to obtain historical weather data. It recieves a JSON response from which it extracts minimum and maximum screen temperatures. If minimum and maximum temperatures are not present it will default to the screen temperature, if there is no recorded data it will record a value of "null". The programme displays the data for the recorded times for each day in the console for the user to see. It then saves the returned data in the local directory as a JSON .txt file. 

The request is made via a https URL to protect user data from interception and checks that the response is JSON as requested in the headers before allowing the programme to compile a Python dictionary of the response.

## List of Modules Used
requests
json
dotenv 
os

To run this file, go to the local directory it is contained in and run:
`python3 ./api.py`

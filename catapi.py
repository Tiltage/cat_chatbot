from dotenv import load_dotenv
import requests, json
import os

load_dotenv()
api_key = os.getenv('CAT_API_KEY')

def call_api(order, breedinfo, breeds, number):
    if breeds[0] == '':
        url = f'https://api.thecatapi.com/v1/images/search?limit={number}&has_breeds={breedinfo}order={order}&api_key={api_key}'
    else:
        breeds =  ','.join(breeds)
        url = f'https://api.thecatapi.com/v1/images/search?limit={number}&breed_ids={breeds}&has_breeds={breedinfo}order={order}&api_key={api_key}'
    response = requests.get(url)
    print(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Error {response.status_code}: Failed to fetch data from API")
        return None

def get_json_obj(order, breedinfo, breeds, number):
    json_data = call_api(order, breedinfo, breeds, number)
    return json_data


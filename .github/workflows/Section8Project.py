import flask
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

class Section8HomeFinder:
    def __init__(self):
        self.base_url = "https://www.hud.gov/program_offices/public_indian_housing/pha/contacts"
        self.affordable_homes_url = "https://www.affordablehousing.com"

    def find_housing_commissions(self, state):
        url = f"{self.base_url}/{state}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        commissions = soup.find_all('div', class_='housing-commission')
        return [commission.text for commission in commissions]

    def search_homes(self, state, city, zip_code, home_type, status):
        url = f"{self.affordable_homes_url}/search"
        params = {
            'state': state,
            'city': city,
            'zip': zip_code,
            'type': home_type,
            'status': status
        }
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        homes = []
        listings = soup.find_all('div', class_='property-listing')
        for listing in listings:
            address = listing.find('h2', class_='property-address').text.strip()
            price = listing.find('span', class_='property-price').text.strip()
            bedrooms = listing.find('span', class_='property-beds').text.strip()
            bathrooms = listing.find('span', class_='property-baths').text.strip()
            
            homes.append({
                'address': address,
                'price': price,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'type': home_type,
                'status': status
            })
        
        return homes

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.json
    state = data.get('state')
    city = data.get('city')
    zip_code = data.get('zip_code')
    home_type = data.get('home_type')
    status = data.get('status')

    finder = Section8HomeFinder()
    homes = finder.search_homes(state, city, zip_code, home_type, status)
    commissions = finder.find_housing_commissions(state)

    return jsonify({
        'homes': homes,
        'commissions': commissions
    })

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)

class HomeFinder:
    def __init__(self):
        self.government_url = "https://www.hud.gov/program_offices/public_indian_housing/pha/contacts"  # Public source
        self.listing_source = "https://publichousing.example.com"  # Example source, replace with your own or public API

    def get_housing_commissions(self, state):
        """Fetches public housing commissions from a government source."""
        url = f"{self.government_url}/{state}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch commissions: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        commissions = soup.find_all('div', class_='housing-commission') or []
        return [commission.text.strip() for commission in commissions]

    def search_homes(self, state, city, zip_code, home_type, status):
        """Searches for homes based on user criteria."""
        url = f"{self.listing_source}/search"
        params = {
            'state': state,
            'city': city,
            'zip': zip_code,
            'type': home_type,
            'status': status
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch homes: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        homes = []
        listings = soup.find_all('div', class_='property-listing') or []
        
        for listing in listings:
            address = listing.find('h2', class_='property-address')
            price = listing.find('span', class_='property-price')
            bedrooms = listing.find('span', class_='property-beds')
            bathrooms = listing.find('span', class_='property-baths')

            if address and price and bedrooms and bathrooms:
                homes.append({
                    'address': address.text.strip(),
                    'price': price.text.strip(),
                    'bedrooms': bedrooms.text.strip(),
                    'bathrooms': bathrooms.text.strip(),
                    'type': home_type,
                    'status': status
                })
        
        return homes


@app.route('/', methods=['GET'])
def home():
    """Home page route."""
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search_page():
    """Search page route."""
    return render_template('search.html')


@app.route('/api/search', methods=['POST'])
def api_search():
    """API for handling search requests."""
    data = request.json
    state = data.get('state')
    city = data.get('city')
    zip_code = data.get('zip_code')
    home_type = data.get('home_type')
    status = data.get('status')

    finder = HomeFinder()
    homes = finder.search_homes(state, city, zip_code, home_type, status)
    commissions = finder.get_housing_commissions(state)

    return jsonify({
        'homes': homes,
        'commissions': commissions
    })


if __name__ == '__main__':
    app.run(debug=True)

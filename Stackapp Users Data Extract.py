import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

base_url = 'https://stackapps.com/users?tab=reputation&filter=all&page='
pages_to_scrape = 25  # Specify the number of pages you want to scrape

users_data = []  # Initialize an empty list to store user information

for page in range(1, pages_to_scrape + 1):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    user_info_elements = soup.find_all('div', class_='user-details')

    for user_info_element in user_info_elements:
        user_link = user_info_element.find('a')
        user_name = user_link.get_text(strip=True)
        user_profile_url = user_link['href']
        user_location = user_info_element.find('span', class_='user-location').get_text(strip=True)
        reputation_score = user_info_element.find('span', class_='reputation-score').get_text(strip=True)
        badges = user_info_element.find('div', class_='-flair')
        
        golds = 0
        silvers = 0
        bronzes = 0

        for badge in badges.find_all('span', class_='badge1'):
            badge_text = badge.find_next('span', class_='badgecount').text.strip()
            golds = int(re.sub('[^0-9]', '', badge_text)) if badge_text else 0

        for badge in badges.find_all('span', class_='badge2'):
            badge_text = badge.find_next('span', class_='badgecount').text.strip()
            silvers = int(re.sub('[^0-9]', '', badge_text)) if badge_text else 0

        for badge in badges.find_all('span', class_='badge3'):
            badge_text = badge.find_next('span', class_='badgecount').text.strip()
            bronzes = int(re.sub('[^0-9]', '', badge_text)) if badge_text else 0

        
        users_data.append({
            'User Name': user_name,
            'Profile URL': user_profile_url,
            'Location': user_location,
            'Reputation Score': reputation_score,
            'Gold Badges': golds,
            'Silver Badges': silvers,
            'Bronze Badges': bronzes
        })

df = pd.DataFrame(users_data)

df.to_csv('Stackapps_Users.csv', index=False)


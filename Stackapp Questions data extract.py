import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

base_url = 'https://stackapps.com/questions?tab=newest&page='
page = 1
data = []

while True:
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    question_summaries = soup.find_all('div', class_='s-post-summary js-post-summary')

    if not question_summaries:
        break  # No more question summaries, exit the loop

    for question in question_summaries:
        title = question.find('a', class_='s-link').text.strip()
        votes_element = question.find('div', class_='s-post-summary--stats-item s-post-summary--stats-item__emphasized')
        votes = votes_element.find('span', class_='s-post-summary--stats-item-number').text.strip() if votes_element else '0'
        answers_element = question.find('div', class_='s-post-summary--stats-item has-answers')
        answers = answers_element.find('span', class_='s-post-summary--stats-item-number').text.strip() if answers_element else '0'
        # Find the views elements
        views_elements = question.find_all('div', class_=re.compile(r's-post-summary--stats-item(\sis-warm)?'))

        views = []
        for view_element in views_elements:
            view_number_element = view_element.find('span', class_='s-post-summary--stats-item-number')
            if view_number_element:
                view_text = view_number_element.text.strip().replace('k', '000')
                views.append(view_text)

        last_view = views[-1] if views else '0'
        
        user_element = question.find('div', class_='s-user-card--link d-flex gs4')
        user = user_element.find('a').text.strip() if user_element and user_element.find('a') else 'Unknown User'

        timestamp_element = question.find('time', class_='s-user-card--time')
        timestamp = timestamp_element.find('span')['title'] if timestamp_element and timestamp_element.find('span') else 'Unknown Timestamp'

        
        data.append({'Question': title, 'Votes': votes, 'Answers': answers, 'Views': last_view, 'User_name': user, 'Timestamp': timestamp})

    page += 1



df = pd.DataFrame(data)
df.to_csv('Stackapps_Questions.csv', index=False)



import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re

base_url = 'https://stackapps.com/tags?page='
page = 8

url = base_url + str(page)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
tags_summaries = soup.find_all('div', class_='grid--item s-card js-tag-cell d-flex fd-column')

tag = []
question = []
asked_this_month = []
asked_this_year = []

for page in range(1, page + 1):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tag_elements = soup.find_all('a', class_='post-tag')
    question_elements = soup.find_all('div', class_='mt-auto d-flex jc-space-between fs-caption fc-black-400')
    ask_this_month_year = soup.find_all('div', class_='flex--item s-anchors s-anchors__inherit')

    tags = [tag.text for tag in tag_elements]

    questions = []
    questions = [re.sub('[^0-9]', '', question.find('div', class_='flex--item').text) for question in question_elements]

    months = []
    for month in ask_this_month_year:
        month_links = month.find_all('a', href='/questions/tagged/script?sort=newest&days=30')
        if len(month_links) > 0:
            month_text = re.sub('[^0-9]', '', month_links[0].text)
        else:
            month_text = '0'
        months.append(month_text)

    years = []
    for year in ask_this_month_year:
        year_links = year.find_all('a')
        year_text = '0'
        for link in year_links:
            if 'questions tagged' in link['title']:
                year_text = re.sub('[^0-9]', '', link.text)
                break
        years.append(year_text)
        
    # Check if the lengths are the same
    length = len(tags)
    if len(questions) != length:
        questions = ['N/A'] * length
    if len(months) != length:
        months = ['N/A'] * length
    if len(years) != length:
        years = ['N/A'] * length

    tag.extend(tags)
    question.extend(questions)
    asked_this_month.extend(months)
    asked_this_year.extend(years)

data = {
    'Tag': tag,
    'Questions': question,
    'Asked This Month': asked_this_month,
    'Asked This Year': asked_this_year
}
df = pd.DataFrame(data)
df.to_csv('Stackapps_Tags.csv', index=False)



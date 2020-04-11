import requests
import spacy
import en_core_web_sm
from bs4 import BeautifulSoup

def update_database(request):
    
    # Initializing variables.
    request_json = request.get_json(silent=True)
    title_tags = []
    orgs = ['bbc.com', 'bloomberg.com', 'buzzfeednews.com', 'cnn.com', 'foxnews.com', 'motherjones.com', 'thewashingtontimes.com', 'vox.com']
    return_string = " "
    
    if request_json and 'url' in request_json:
    
        # Getting the title of the article.
        html_content = requests.get(request_json['url']).content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        if request_json['url'].find('breitbart.com'):
            title = soup.find('h1').text
        else:
            for org in orgs:
                if org in request_json['url']:
                    title = soup.find('h1', class_ = request_json['classInfo']).text
        
        # Getting the tags from the title.
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(title)
        for token in doc:
            if token.pos_ == 'PROPN' or token.pos_ == 'NOUN':
                title_tags.append(token.text)

    return_string = return_string.join(title_tags)
    return return_string
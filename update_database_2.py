import requests
from bs4 import BeautifulSoup
from google.cloud import firestore

def update_database(request):
    
    # Initializing variables.
    db = firestore.Client()
    request_json = request.get_json(silent=True)
    database_tags = []
    banned = ['Error:', 'Error', 'BBC', 'Homepage', 'could', 'not', 'handle', 'the', 'request\n', 'Google', 'Accounts', 'account', 'Request', 'Firestore']
    
    if request_json and 'tags' in request_json:
        
        # Getting tags already in the database.
        tags_ref = db.collection(str(request_json['id']) + '-tags')
        tags = tags_ref.stream()
        for tag in tags:
            database_tags.append(tag.id)
            
        # Adding tags to database if it doesn't exist, otherwise it increments the appropriate tag.
        title_tags = request_json['tags'].split(' ')       
        for tag in title_tags:
            if tag not in banned:
                if tag not in database_tags:
                    tags_ref.document(tag).set({u'count': 1})
                else:
                    tags_ref.document(tag).update({u'count': tags_ref.document(tag).get().to_dict()['count'] + 1})
        
        # Incrementing the appropriate news organization in database or creating if doesn't exist.
        news_ref = db.collection(str(request_json['id']) + '-news organizations')
        if news_ref.document(u'bbc').get().exists:
            orgs = news_ref.stream()
            for org in orgs:
                if request_json['url'].find(org.to_dict()['url']) != -1:
                    news_ref.document(org.id).update({u'count': org.to_dict()['count'] + 1})
        else:
            news_ref.document(u'bbc').set({u'count': 0, u'political bias': 0, u'url': u'bbc.com'})
            news_ref.document(u'bloomberg').set({u'count': 0, u'political bias': 0, u'url': u'bloomberg.com'})
            news_ref.document(u'breitbart').set({u'count': 0, u'political bias': -1, u'url': u'breitbart.com'})
            news_ref.document(u'buzzfeed').set({u'count': 0, u'political bias': 1, u'url': u'buzzfeednews.com'})
            news_ref.document(u'cnn').set({u'count': 0, u'political bias': 0.5, u'url': u'cnn.com'})
            news_ref.document(u'fox news').set({u'count': 0, u'political bias': -0.5, u'url': u'foxnews.com'})
            news_ref.document(u'mother jones').set({u'count': 0, u'political bias': 1, u'url': u'motherjones.com'})
            news_ref.document(u'the washington times').set({u'count': 0, u'political bias': -0.5, u'url': u'washingtontimes.com'})
            news_ref.document(u'vox').set({u'count': 0, u'political bias': 1, u'url': u'vox.com'})
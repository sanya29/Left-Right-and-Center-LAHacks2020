import requests
from bs4 import BeautifulSoup
from google.cloud import firestore
from googlesearch import search

def retrieve_from_database(request):
    
    request_json = request.get_json(silent=True)
    
    # Initializing variables.
    pb_score = 0
    political_view = ""
    db = firestore.Client()
    id = request_json['id']
    database_tags = []
    database_tag_dict = {}
    num_tags = 0
    
    # Getting tags and respective counts in the database.
    database_tags.clear()
    tags_ref = db.collection(id + '-tags')
    tags = tags_ref.stream()
    for tag in tags:
        num_tags += 1
        database_tag_dict[tag.id] = tags_ref.document(tag.id).get().to_dict()['count']
    if num_tags < 3:
        return 'not_enough_tags'
        
    # Get the most frequent tags.
    first_most_frequent_tag = max(database_tag_dict, key = database_tag_dict.get)
    database_tag_dict.pop(first_most_frequent_tag)
    second_most_frequent_tag = max(database_tag_dict, key = database_tag_dict.get)
    if tags_ref.document(first_most_frequent_tag).get().to_dict()['count'] < 4 or tags_ref.document(second_most_frequent_tag).get().to_dict()['count'] < 4:
        return 'not_enough_tags'
    
    # Compute political bias score and get most frequent news organization.
    news_ref = db.collection(id + '-news organizations')
    org_max_count = 0
    org_min_count = 1000000
    total_pb_score = 0
    most_frequent_org = ""
    least_frequent_org = ""
    for org in news_ref.stream():
        pb_score = pb_score + org.to_dict()['count'] * org.to_dict()['political bias']
        total_pb_score = total_pb_score + 1 * org.to_dict()['count']
        if org.to_dict()['count'] > org_max_count:
            org_max_count = org.to_dict()['count']
            most_frequent_org = org.id     
    try:
        pb_score = pb_score / total_pb_score
    except:
        return 'not_enough_tags'
    for org in news_ref.stream():
        if org.to_dict()['political bias'] == -1 * news_ref.document(most_frequent_org).get().to_dict()['political bias']:
            if org.to_dict()['count'] < org_min_count:
                least_frequent_org = org.id
                org_min_count = org.to_dict()['count']
    
    # Finding political ideology.
    if pb_score >= -1 and pb_score < -0.8:
        political_view = 'leaning far right'
    elif pb_score >= -0.8 and pb_score < -0.2:
        political_view = 'leaning right'
    elif pb_score > 0.2 and pb_score <= 0.8:
        political_view = 'leaning left'
    elif pb_score > 0.8 and pb_score <= 1:
        political_view = 'leaning far left'
    else:
        political_view = 'centre'    
    
    # Getting new articles.
    count = 0
    query = least_frequent_org + ' ' + first_most_frequent_tag + ' ' + second_most_frequent_tag
    news_articles = search(query, stop = 20)
    articles_for_user = []
    for article in news_articles:
        if article.find(least_frequent_org) != -1:
            articles_for_user.append(article)
            count += 1
        if count == 3:
            break
    
    # Constructing return string.
    return_string = articles_for_user[0] + '~' + articles_for_user[1] + '~' + articles_for_user[2] + '~' + most_frequent_org + '~' + political_view + '~' + first_most_frequent_tag + '~' + second_most_frequent_tag
    return return_string
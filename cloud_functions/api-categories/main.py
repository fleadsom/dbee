import json
from google.cloud import firestore
# def load_from_firestore():
#     db = firestore.Client()
#     categoryRef = db.collection(u'category_weights')

#     for doc in doc_ref.stream():
#         print(f'{doc.id} => {doc.to_dict()}')
    

def api_categories(request):
    
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """



    
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)
    # db = firestore.Client()
    # categoryRef = db.collection(u'category_weights')
    # for doc in categoryRef.stream():
    #     print(f'{doc.id} => {doc.to_dict()}')

    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    result = []
    db = firestore.Client()
    categoryRef = db.collection(u'category_weights').get()
    for doc in categoryRef:
        dic = doc.to_dict()
        print(f'{doc.id} => {doc.to_dict()}')
        dic['category'] = dic.pop('name')
        dic['score'] = dic.pop('weight')
        result.append(dic)
    return(json.dumps(result),200,headers)

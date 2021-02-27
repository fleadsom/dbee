from google.cloud import firestore
import json

def get_emails(request):
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

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # connect to firestore
    db = firestore.Client()

    emails_list = db.collection(u'emails').get()
    print(emails_list)
    result_list = []
    category = request.args.get('category')
    for email in emails_list:
        try:
            if category in email.get('categories'):
                email_dic = email.to_dict()
                email_dic['id'] = email.id
                result_list.append(email_dic)
            print(result_list)
        except KeyError as e:
            print(e)

    return (json.dumps(result_list), 200, headers)

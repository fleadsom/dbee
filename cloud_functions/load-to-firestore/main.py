def load_to_firestore(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    from google.cloud import storage
    from google.cloud import firestore
    from google.cloud import pubsub_v1
    import json

    def download_json(bucket_name, source_blob_name):

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.get_blob(source_blob_name)
        data = json.loads(blob.download_as_string(client=None))

        return data

    def load_to_firestore(data):

        db = firestore.Client()

        for email in data:
            message_id = email["Message ID"]
            subject = email["Subject"]
            sender = email["From"]
            text = email["Email Text"]
            timestamp = email["Date & Time Received"]
            #categories = email["Categories"]
            
            # Add a new document
            doc_ref = db.collection(u'emails').document(u'{}'.format(message_id))
            doc_ref.set({
                u'from': u'{}'.format(sender),
                u'subject': u'{}'.format(subject),
                u'text': u'{}'.format(text),
                u'timestamp': u'{}'.format(timestamp)#,
                #u'categories': categories
            })

    data = download_json('email_staging','emaildata.json')
    load_to_firestore(data)

    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id='hack-hackasaumon',
        topic='categories-trigger',  # Set this to something appropriate.
    )
    future = publisher.publish(topic_name, b'Done loading messages into Firestore')
    future.result()

    return f'Hello World!'
   
def add_category_weights(event, context):

    from google.cloud import storage
    from google.cloud import firestore
    from google.cloud import pubsub_v1


    def list_categories(bucket_name, source_blob_name):

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.get_blob(source_blob_name)
        categories = blob.download_as_string(client=None).decode('utf-8').split(',')

        return categories

    def create_weights(list_of_categories, collection):

        db = firestore.Client()
        emails_list = db.collection(u'{}'.format(collection)).get()
        
        print(list_of_categories)
        other_category = 'other'

        dict_of_weights = {}
        for category in list_of_categories:
            dict_of_weights[category] = 0
        print(dict_of_weights)
        
        for email in emails_list:
            categories = email.get("categories")

            for category in categories:
                dict_of_weights[category] = dict_of_weights[category] + 1
        
        print(dict_of_weights)
        
        for category in list_of_categories:
            # Add a new document
            doc_ref = db.collection(u'category_weights').document(u'{}'.format(category))
            doc_ref.set({
                u'name': u'{}'.format(category),
                u'weight': dict_of_weights[category]
            })

    list_of_categories = list_categories('email_staging', 'list-of-categories.txt')
    create_weights(list_of_categories, 'emails')

    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id='hack-hackasaumon',
        topic='sentiment-trigger',  # Set this to something appropriate.
    )
    future = publisher.publish(topic_name, b'Done adding weights')
    future.result()
    return f'Weights added to Firestore!'

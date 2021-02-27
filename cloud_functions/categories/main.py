from google.cloud import storage
from google.cloud import firestore
from google.cloud import pubsub_v1
import json

#Create list of categories
def list_categories(bucket_name, source_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(source_blob_name)
    categories = blob.download_as_string(client=None).decode('utf-8').split(',')

    return categories


#Read data from firestore and adds categories directly in firestore
def read_data_and_add_categories(collection, list_of_categories, other_category):

    db = firestore.Client()
    emails_list = db.collection(u'{}'.format(collection)).get()

    categories_per_email = [[] for i in range(len(emails_list))]

    for i in range(len(emails_list)):
        email = emails_list[i]

        subject = email.get('subject')
        subject = subject.lower()
        body = email.get('text')
        body = body.lower()
        count=0
        for keyword in list_of_categories:
            if ((keyword in subject) or (keyword in body)):
                categories_per_email[i].append(keyword)
            else:
                count+=1
        if count==len(list_of_categories):
            categories_per_email[i].append(other_category)
                

    for i in range(len(emails_list)):
        email = emails_list[i]
        message_id = email.id

        doc_ref = db.collection(u'{}'.format(collection)).document(u'{}'.format(message_id))
        doc_ref.update({
            u'categories': categories_per_email[i]
        })



def add_categories(event, context):

    list_of_categories = list_categories('email_staging', 'list-of-categories.txt')

    read_data_and_add_categories('emails', list_of_categories, 'other')

    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id='hack-hackasaumon',
        topic='weights-trigger',  # Set this to something appropriate.
    )
    future = publisher.publish(topic_name, b'Done adding categories')
    future.result()

    return 'Updated categories'
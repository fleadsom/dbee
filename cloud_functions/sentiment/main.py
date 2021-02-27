def sentiment_analysis(event, context):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    from google.cloud import language_v1
    from google.cloud import firestore
    import json


    def read_data_and_add_sentiment(collection):

        db = firestore.Client()

        emails_list = db.collection(u'{}'.format(collection)).get()
        for email in emails_list:
            sentiment, magnitude = analyze_sentiment(email.get('text'))
            message_id = email.id

            doc_ref = db.collection(u'{}'.format(collection)).document(u'{}'.format(message_id))
            doc_ref.update({
                u'sentiment': sentiment,
                u'magnitude': magnitude
            })
        
    

    def analyze_sentiment(text):
        # Instantiates a client
        client = language_v1.LanguageServiceClient()

        # The text to analyze
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

        print("Text: {}".format(text))
        print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

        return(sentiment.score, sentiment.magnitude)

        
    read_data_and_add_sentiment('emails')

    text = u"Hello, world!"
    score, magnitude = analyze_sentiment(text)

    return 'Score: ' + str(score) + ', Magnitude: ' + str(magnitude)

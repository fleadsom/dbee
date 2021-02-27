const Auth = require('@google-cloud/express-oauth2-handlers');
const {Datastore} = require('@google-cloud/datastore');
const {Firestore} = require('@google-cloud/firestore');
const {PubSub} = require('@google-cloud/pubsub');
const {google} = require('googleapis');
const gmail = google.gmail('v1');

const datastoreClient = new Datastore();
const firestoreClient = new Firestore();

const requiredScopes = [
  'profile',
  'email',
  'https://www.googleapis.com/auth/gmail.modify'
];

const auth = Auth('datastore', requiredScopes, 'email', true);

const checkForDuplicateNotifications = async (messageId) => {
  const transaction = datastoreClient.transaction();
  await transaction.run();
  const messageKey = datastoreClient.key(['emailNotifications', messageId]);
  const [message] = await transaction.get(messageKey);
  if (!message) {
    await transaction.save({
      key: messageKey,
      data: {}
    });
  }
  await transaction.commit();
  if (!message) {
    return messageId;
  }
};

const getMostRecentMessageWithTag = async (email, historyId) => {
  // Look up the most recent message.
  const listMessagesRes = await gmail.users.messages.list({
    userId: email,
    maxResults: 1
  });
  const messageId = await checkForDuplicateNotifications(listMessagesRes.data.messages[0].id);

  // Get the message using the message ID.
  if (messageId) {
    const message = await gmail.users.messages.get({
      userId: email,
      id: messageId
    });

    return message;
  }
};

// Extract message ID, sender, attachment filename and attachment ID
// from the message.
const extractInfoFromMessage = (message) => {
  const messageId = message.data.id;
  let from;
  let subject;
  let body;

  const headers = message.data.payload.headers;
  for (var i in headers) {
    if (headers[i].name === 'From') {
      from = headers[i].value;
    }
    if (headers[i].name === 'Subject') {
      subject = headers[i].value;
    }
  }

  body = message.data.snippet;

  return {
    messageId: messageId,
    from: from,
    subject: subject,
    text: body,
    timestamp: message.data.internalDate
  };
};

exports.watchGmailMessages = async (event) => {
  // Decode the incoming Gmail push notification.
  const data = Buffer.from(event.data, 'base64').toString();
  const newMessageNotification = JSON.parse(data);
  const email = newMessageNotification.emailAddress;
  const historyId = newMessageNotification.historyId;

  try {
    await auth.auth.requireAuth(null, null, email);
  } catch (err) {
    console.log('An error has occurred in the auth process.');
    throw err;
  }
  const authClient = await auth.auth.authedUser.getClient();
  google.options({auth: authClient});

  // Process the incoming message.
  const message = await getMostRecentMessageWithTag(email, historyId);
  if (message) {
    const messageInfo = extractInfoFromMessage(message);
    if (messageInfo.from) {
      if (await firestoreClient.collection('emails').doc(messageInfo.messageId).set(messageInfo)) {
        console.log('success');
        const pubsub = new PubSub();
        await pubsub.topic('categories-trigger').publish(Buffer.from('start categories!'))
      }
    }
  }
};

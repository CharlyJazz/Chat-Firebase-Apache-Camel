// Interface for sending a message
interface CreateMessagePayload {
  body: string;
  from_user: string;
  to_user: string;
  chat_id: string;
}

// Interface for validating getting messages
interface GetMessageValidator {
  chat_id: string;
  quantity?: number;
  time?: string | null;
}

// Main interface that defined a Message
interface MessageSchema {
  message_id: string;
  from_user: string;
  to_user: string;
  body: string;
  chat_id: string;
  time: string;
  time_iso: string; // DateTime ISO Format
}

interface FirestoreNewMessageContract {
  chat_id: string;
  from_user: string;
  latest_message_time_iso: string;
  list_of_messages: MessageSchema[];
}

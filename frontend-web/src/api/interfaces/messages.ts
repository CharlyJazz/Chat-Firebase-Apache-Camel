// Interface for sending a message
interface MessageSentREST {
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

// Interface for the response when a message is created
interface MessageCreatedResponse {
  message_id: string;
  from_user: string;
  to_user: string;
  body: string;
  chat_id: string;
  time: string;
}

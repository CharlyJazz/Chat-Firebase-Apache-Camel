// Interface for creating a new chat
interface ChatSentREST {
  users_id: string[]; // List of user IDs involved in the chat
}

// Interface for the response when a chat is created or when sending a message
interface ChatCreatedResponse {
  chat_id: string; // Unique identifier for the chat
  users_id: string[]; // List of user IDs involved in the chat
  users_name: string[]; // List of user names involved in the chat
}

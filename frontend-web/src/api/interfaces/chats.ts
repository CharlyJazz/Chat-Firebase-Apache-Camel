type CHAT_ALREADY_EXIST_MSG = "There is a chat for this users";

// Interface for the response when a chat is created or when sending a message
interface ChatSchema {
  chat_id: string; // Unique identifier for the chat
  users_id: string[]; // List of user IDs involved in the chat
  users_name: string[]; // List of user names involved in the chat
}

// Interface for creating a new chat
interface ChatSentREST extends Pick<ChatSchema, "users_id" | "users_name"> {}

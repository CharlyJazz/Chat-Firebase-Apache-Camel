import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed
import { useState } from "react";

const useCreateChat = () => {
  const uri = `${process.env.NEXT_PUBLIC_CHAT_MICROSERVICE}/api/v1/chat/`;
  const [error, setError] = useState<string | undefined>();
  const [data, setData] = useState<ChatSchema>();
  const [loading, setLoading] = useState<boolean>(false);

  const createChat = async (chatData: ChatSentREST) => {
    try {
      setLoading(true);
      const response = await fetcher<ChatSchema>(uri, "POST", chatData);
      setData(response);
    } catch (error) {
      setError("There was an error creating the Chat");
    } finally {
      setLoading(false);
    }
  };

  return {
    createChat,
    errorCreatingChat: error,
    chatCreated: data,
    chatCreationLoading: loading,
  };
};

export default useCreateChat;

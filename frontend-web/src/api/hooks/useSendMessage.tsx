import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed
import { useState } from "react";

const useSendMessage = () => {
  const uri = `${process.env.NEXT_PUBLIC_CHAT_MICROSERVICE}/api/v1/messaging/`;
  const [error, setError] = useState<string | undefined>();
  const [data, setData] = useState<MessageCreatedResponse>();
  const [loading, setLoading] = useState<boolean>(false);

  const sendMessage = async (messageData: CreateMessagePayload) => {
    try {
      setLoading(true);
      const response = await fetcher<MessageCreatedResponse>(
        uri,
        "POST",
        messageData
      );
      setData(response);
      setError(undefined);
    } catch (error: unknown) {
      if ((error as Error).message) {
        setError((error as Error).message);
      }
    } finally {
      setLoading(false);
    }
  };

  return {
    sendMessage,
    sendMessageError: error,
    messageSent: data,
    sendingMessage: loading,
  };
};

export default useSendMessage;

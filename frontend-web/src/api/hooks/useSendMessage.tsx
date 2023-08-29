import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed
import { useState } from "react";
import { KeyedMutator } from "swr";

const useSendMessage = () => {
  const uri = `${process.env.NEXT_PUBLIC_CHAT_MICROSERVICE}/api/v1/messaging/`;
  const [error, setError] = useState<string | undefined>();
  const [data, setData] = useState<MessageSchema>();
  const [loading, setLoading] = useState<boolean>(false);

  const sendMessage = async (
    messageData: CreateMessagePayload,
    mutate?: KeyedMutator<MessageSchema[]>
  ) => {
    try {
      setLoading(true);
      const response = await fetcher<MessageSchema>(uri, "POST", messageData);
      setData(response);
      setError(undefined);
      mutate && mutate();
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

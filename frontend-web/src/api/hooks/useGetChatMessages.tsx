import useSWR, { mutate } from "swr";
import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed

interface GetMessageValidator {
  chat_id: string;
  quantity?: number;
  time?: string | null;
}

const useGetChatMessages = (params?: GetMessageValidator) => {
  const { chat_id, quantity, time } = params || {};

  let uri = "";
  if (chat_id) {
    uri = `${process.env.NEXT_PUBLIC_CHAT_MICROSERVICE}/api/v1/chat/${chat_id}/messages`;
    if (quantity !== undefined) {
      uri += `?quantity=${quantity}`;
    }
    if (time !== undefined) {
      uri += quantity !== undefined ? `&time=${time}` : `?time=${time}`;
    }
  }

  const {
    data,
    error,
    isValidating: loading,
    mutate,
  } = useSWR<MessageSchema[]>(chat_id ? uri : null, fetcher);

  return {
    messagesData: data || [],
    messagesError: error,
    messagesLoading: loading,
    mutate: mutate,
  };
};

export default useGetChatMessages;

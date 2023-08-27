import useSWR from "swr";
import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed

const useGetChatMessages = () => {
  // use swr
  // url = `${NEXT_PUBLIC_CHAT_MICROSERVICE}/api/v1/chat/:chatId`

  return {
    // return data, error and loading attributes
  };
};

export default useGetChatMessages;

// Import the necessary dependencies
import useSWR from "swr";
import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed

const useGetCurrentUserChats = () => {
  const {
    data: chatsData,
    error: chatsError,
    isLoading: chatsLoading,
  } = useSWR<ChatSchema[]>(
    `${process.env.NEXT_PUBLIC_CHAT_MICROSERVICE}/api/v1/chat/`,
    fetcher
  );

  return {
    chatsData: chatsData || [],
    chatsError,
    chatsLoading,
  };
};

export default useGetCurrentUserChats;

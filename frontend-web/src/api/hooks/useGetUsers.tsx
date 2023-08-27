import useSWR from "swr";
import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed

const useGetUsers = () => {
  const {
    data: usersData,
    error: usersError,
    isLoading: usersLoading,
  } = useSWR<User[]>(
    `${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/users`,
    fetcher
  );

  return {
    usersData,
    usersError,
    usersLoading,
  };
};

export default useGetUsers;

import { fetcher } from "@/lib/swr-fetcher"; // Update the import path as needed
import { useState } from "react";

const useCreateUser = () => {
  const [error, setError] = useState<string | undefined>();
  const [loading, setLoading] = useState<boolean>(false);
  const [userCreated, setUserCreated] = useState<UserCreatedResponse>();

  const createAccount = async (userData: CreateUserPayload): Promise<void> => {
    try {
      setLoading(true);
      const response = await fetcher<UserCreatedResponse>(
        `${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/users/`,
        "POST",
        {
          username: userData.username,
          password: userData.password,
        }
      );

      if (response.detail) {
        setError(response.detail);
      } else {
        setUserCreated(response);
        setError(undefined);
      }
    } catch (error) {
      setError((error as Error)?.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    createAccount,
    userCreated,
    errorCreatingAccount: error,
    accountCreationLoading: loading,
  };
};

export default useCreateUser;

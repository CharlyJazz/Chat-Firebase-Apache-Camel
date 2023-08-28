import { fetcher } from "@/lib/swr-fetcher";
import { useState } from "react";

const useLoginRequest = () => {
  const [error, setError] = useState<string | undefined>();
  const [loading, setLoading] = useState<boolean>(false);
  const [authenticatedUserResponse, setResponse] =
    useState<AuthenticatedUserResponse>();

  const loginRequest = async (credentials: LoginPayload) => {
    try {
      setLoading(true);
      setError(undefined);

      const response = await fetcher<AuthenticatedUserResponse>(
        `${process.env.NEXT_PUBLIC_AUTH_MICROSERVICE}/api/v1/login`,
        "POST",
        {
          username: credentials.username,
          password: credentials.password,
        },
        {
          "Content-Type": "application/x-www-form-urlencoded",
        }
      );

      if (response.detail) {
        setError(response.detail);
      } else {
        setResponse(response);
      }
    } catch (error) {
      setError((error as Error)?.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    errorLogin: error,
    loadingLogin: loading,
    authenticatedUserResponse,
    loginRequest,
  };
};

export default useLoginRequest;

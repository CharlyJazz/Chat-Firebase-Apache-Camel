interface CreateUserPayload {
  username: string;
  password: string;
}

interface AuthenticatedUserResponse {
  access_token: string;
  token_type: string;
  username: string;
  id: string;
  detail?: string;
}

interface UserCreatedResponse {
  id: number;
  username: string;
  detail?: string;
}

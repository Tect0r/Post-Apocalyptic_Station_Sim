export type RegisterRequest = {
  email: string;
  username: string;
  password: string;
};

export type LoginRequest = {
  email: string;
  password: string;
};

export type AuthResponse = {
  success: boolean;
  message: string;
  data: {
    access_token?: string;
    token_type?: string;
    user_id?: string;
    player_id?: string;
    username?: string;
    email?: string;
  } | null;
};
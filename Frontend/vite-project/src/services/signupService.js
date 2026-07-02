import api from "../api/axios";

export const signupUser = async (email, password) => {
  const response = await api.post("/auth/signup", {
    email,
    password,
  });

  return response.data;
};
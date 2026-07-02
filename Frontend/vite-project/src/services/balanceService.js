import api from "../api/axios";

const getToken = () => localStorage.getItem("token");

const authHeader = () => ({
  headers: {
    Authorization: `Bearer ${getToken()}`,
  },
});

export const getOverallBalance = async () => {
  const response = await api.get(
    "/balances/overall",
    authHeader()
  );

  return response.data;
};

export const getGroupBalances = async (groupId) => {
  const response = await api.get(
    `/balances/${groupId}`,
    authHeader()
  );

  return response.data;
};

export const getSimplifiedBalances = async (groupId) => {
  const response = await api.get(
    `/balances/${groupId}/simplified`,
    authHeader()
  );

  return response.data;
};
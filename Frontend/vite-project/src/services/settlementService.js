import api from "../api/axios";

const getToken = () => localStorage.getItem("token");

const authHeader = () => ({
  headers: {
    Authorization: `Bearer ${getToken()}`,
  },
});

export const createSettlement = async (data) => {
  const response = await api.post(
    "/settlements",
    data,
    authHeader()
  );

  return response.data;
};

export const getSettlementHistory = async (groupId) => {
  const response = await api.get(
    `/settlements/${groupId}`,
    authHeader()
  );

  return response.data;
};
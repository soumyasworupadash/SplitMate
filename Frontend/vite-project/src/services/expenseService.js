import api from "../api/axios";

const getToken = () => localStorage.getItem("token");

const authHeader = () => ({
  headers: {
    Authorization: `Bearer ${getToken()}`,
  },
});

export const getExpenses = async (groupId) => {
  const response = await api.get(
    `/expenses/group/${groupId}`,
    authHeader()
  );

  return response.data;
};

export const createExpense = async (expense) => {
  const response = await api.post(
    "/expenses",
    expense,
    authHeader()
  );

  return response.data;
};

export const updateExpense = async (
  expenseId,
  expense
) => {
  const response = await api.put(
    `/expenses/${expenseId}`,
    expense,
    authHeader()
  );

  return response.data;
};

export const deleteExpense = async (
  expenseId
) => {
  const response = await api.delete(
    `/expenses/${expenseId}`,
    authHeader()
  );

  return response.data;
};
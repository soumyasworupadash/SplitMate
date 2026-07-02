import api from "../api/axios";

export const getDashboardSummary = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/dashboard/summary", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};

export const getMyActivity = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get("/activity/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
};
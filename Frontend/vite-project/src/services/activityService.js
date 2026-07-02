import api from "../api/axios";

const getToken = () => localStorage.getItem("token");

export const getActivity = async (groupId) => {
  const response = await api.get(
    `/activity/${groupId}`,
    {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );

  return response.data;
};
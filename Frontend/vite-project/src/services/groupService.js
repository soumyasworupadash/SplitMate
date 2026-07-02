import api from "../api/axios";

const getToken = () => localStorage.getItem("token");

export const getGroups = async () => {
  const response = await api.get("/groups", {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  return response.data;
};

export const createGroup = async (name) => {
  const response = await api.post(
    "/groups",
    {
      name,
    },
    {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );

  return response.data;
};

export const deleteGroup = async (groupId) => {
  const response = await api.delete(`/groups/${groupId}`, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  return response.data;
};

export const getGroupMembers = async (groupId) => {
  const response = await api.get(`/groups/${groupId}/members`, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  return response.data;
};

export const addMember = async (groupId, email) => {
  const response = await api.post(
    `/groups/${groupId}/members`,
    {
      email,
    },
    {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );

  return response.data;
};

export const removeMember = async (groupId, userId) => {
  const response = await api.delete(
    `/groups/${groupId}/members/${userId}`,
    {
      headers: {
        Authorization: `Bearer ${getToken()}`,
      },
    }
  );

  return response.data;
};
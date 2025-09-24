import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";

export const useAxios = () => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const [axiosInstance, setAxiosInstance] = useState(null);

  useEffect(() => {
    if (isAuthenticated) {
      getAccessTokenSilently()
        .then((token) => {
          const instance = axios.create({
            baseURL: process.env.REACT_APP_API_URL,
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
          });

          // ✅ attach token correctly
          instance.defaults.headers.common["Authorization"] = `Bearer ${token}`;

          setAxiosInstance(instance);
        })
        .catch((error) => {
          console.error("Error getting token:", error);
          setAxiosInstance(null);
        });
    }
  }, [isAuthenticated, getAccessTokenSilently]);

  return axiosInstance;
};

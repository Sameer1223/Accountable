import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';
import { useEffect, useState } from 'react';

export const useAxios = () => {
    const { getAccessTokenSilently, isAuthenticated } = useAuth0();

    const[token, setToken] = useState('');
    const [axiosInstance, setAxiosInstance] = useState(null);


    useEffect(()=>{
        if (isAuthenticated) {
            getAccessTokenSilently()
            .then(token =>  {
                const instance = axios.create({
                    baseURL: 'http://localhost:3000',
                    headers: {
                        'Content-Type': 'application/json',
                        Accept: 'application/json'
                    }
                });
                instance.defaults.headers.Authorization = `Bearer ${token}`;
                setAxiosInstance({instance});
            })
            .catch(error => {
                console.log(error);
                setAxiosInstance(null);
            })
        }
    }, [isAuthenticated])

    return axiosInstance? axiosInstance.instance : null;
};
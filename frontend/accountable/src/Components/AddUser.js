import { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { useAxios } from '../AxiosInstance';

const AddUser = () => {
    const { user, isAuthenticated } = useAuth0();
    const axiosInstance = useAxios();

    useEffect(() => {
        const addUserToDatabase = async () => {
        if (isAuthenticated && axiosInstance) {
            try {
                const user_id = user.sub.split('|')[1].toString();

                const data = {
                    "user_id": user_id,
                    "name": user.name,
                    "email": user.email
                }
                
                axiosInstance.post('/users', data)
                .then(response => {
                    console.log('User data', response.data);
                })
                .catch(error => {
                    console.log(data);
                    console.error('Failed to add user: ', error);
                });
                
                
            } catch (error) {
            console.error('Error adding user:', error);
            }
        }
    };

    addUserToDatabase();
  }, [isAuthenticated, user, axiosInstance]);

  return null;
};

export default AddUser;

import './GroupsView.css';
import { useEffect, useState, useCallback } from 'react';
import Group from '../Components/Group.js';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import { useAxios } from '../AxiosInstance.js';
import Login from '../Components/Login.js';

function GroupsView({ setFilter }) {
    const axiosInstance = useAxios();

    const [groups, setGroups] = useState([]);
    const [groupName, setGroupName] = useState('');
    const [adding, setAdding] = useState(false);
    const { user, isAuthenticated } = useAuth0();
    const navigate = useNavigate();

    const getUserGroups = useCallback(async () => {
        try {
            // Sanitize user id
            const user_id = user.sub.split('|')[1].toString();
            
            const response = await axiosInstance.get(`/users/${user_id}`);
            const groups = response.data.user.groups;
        
            if (!groups) {
                return;
            }
        
            let groupIds = response.data.user.groups.split(',');
            
            const requests = groupIds.map((id) => axiosInstance.get(`/groups/${id}`));
        
            // Wait for all requests to complete
            const responses = await Promise.all(requests);
        
            // Extract and store group data
            const fetchedData = responses.map((response) => [
                response.data.group.g_id,
                response.data.group.g_name,
                response.data.group.number_of_members
            ]);
            setGroups(fetchedData); // Update state with the fetched data
        } catch (error) {
            console.error("There was an error fetching the data:", error);
        }
    }, [axiosInstance, user, setGroups]);

    const createGroup = async (e) => {
        e.preventDefault();

        // Sanitize user id
        const user_id = user.sub.split('|')[1].toString();

        const data = {
            "name": groupName,
            "owner": user_id
        }

        axiosInstance.post(`/groups`, data)
        .then(response => {
            axiosInstance.patch(`/users/${user_id}/groups/${response.data.group.g_id}`)
            .then(response => {
                console.log('Group added');
                setAdding(false);
                navigate('/');
            })
        })
        .catch(error => {
            console.error('There was an error creating the group:', error);
        });
    };

    useEffect(() => {
        if (isAuthenticated && axiosInstance){
            getUserGroups();
        }
    }, [adding, isAuthenticated, axiosInstance, getUserGroups]);
    
    return (
        <div className='groups-view'>
            <Login/>
            {isAuthenticated && (
                <>
                    <Group id={0} group="Individual" setFilter={setFilter}/>
                    {groups.map((group, index) => (
                        <Group key={index} id={group[0]} group={group[1]} count={group[2]} setFilter={setFilter}/>
                    ))}
                    {adding && 
                    <div>
                        <input type="text" id="name" onChange={(e) => setGroupName(e.target.value)} required/>
                        <button onClick={createGroup}>Add</button>
                    </div>}
                    <button className="add-group-button" onClick={() => setAdding(true)}>+</button>
                </>
            )}
        </div>
    );
}

export default GroupsView;
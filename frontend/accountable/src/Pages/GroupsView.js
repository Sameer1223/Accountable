import './GroupsView.css';
import axios from 'axios';
import { useEffect, useState } from 'react';
import Group from '../Components/Group.js';

function GroupsView({ setFilter }) {  
    const [groups, setGroups] = useState([]);

    const getUserGroups = async () => {
        let temp = [];
        // Get users groups
        axios.get(`/users/${1}`)
        .then(response => {
            let groupIds = response.data.user.groups.split(',');
            groupIds.map((id) => {
                axios.get(`/groups/${id}`)
                .then(response => {
                    temp.push([id, response.data.group.g_name]);
                    setGroups(temp);
                })
                .catch(error => {
                    console.error('There was an error fetching the data:', error);
                });
            })
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    useEffect(() => {
        getUserGroups();
    }, []);
    
    return (
        <div className='groups-view'>
            <Group id={0} group="Individual" setFilter={setFilter}/>
            {groups.map((group, index) => (
                <Group key={index} id={group[0]} group={group[1]} setFilter={setFilter}/>
            ))}
        </div>
    );
}

export default GroupsView;
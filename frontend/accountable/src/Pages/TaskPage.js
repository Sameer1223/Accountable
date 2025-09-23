import './TaskPage.css';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react";
import Task from '../Components/Task.js';
import Progress from '../Components/Progress.js';
import { useAuth0 } from '@auth0/auth0-react';
import { useAxios } from '../AxiosInstance.js';

function TaskPage({ filter }) {
    const axiosInstance = useAxios();

    const [tasks, setTasks] = useState([]);
    const [groupCount, setGroupCount] = useState(0);
    const [isOwner, setIsOwner] = useState(false);
    const [invite, setInvite] = useState('');
    const { user, isAuthenticated } = useAuth0();
    const [adding, setAdding] = useState(false);
    const [lastChecked, setLastChecked] = useState(-1);

    const navigate = useNavigate();

    const goToAddPage = () => {
      navigate('/add');
    };

    const updateLastChecked = async() => {
        // Sanitize user id
        const user_id = user.sub.split('|')[1].toString();

        // Get user last checked date
        axiosInstance.get(`/users/${user_id}`)
        .then(response => {
            const today = new Date();
            let pythonEquivalent = (today.getDay() + 6) % 7;
            
            let last_checked = response.data.user.last_checked;
            setLastChecked(last_checked);
            console.log(last_checked, pythonEquivalent);

            // If mismatch in day reset @TODO: Known bug, same day next week will not reset
            if (last_checked !== null && last_checked !== pythonEquivalent) {
                console.log("we are resetting");
                axiosInstance.patch(`/update-streaks/${user_id}`)
                .then(response => {
                    console.log('Reset');
                })
                .catch(error => {
                    console.error('There was an error fetching the data:', error);
                });
            }

            // Set last checked time for user    
            axiosInstance.patch(`/users/${user_id}`)
            .then(response => {
                console.log('Set last checked');
            })
            .catch(error => {
                console.error('There was an error setting the data:', error);
            });
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    const getTasks = async () => {
        // Sanitize user id
        const user_id = user.sub.split('|')[1].toString();
        
        // Get todays tasks
        axiosInstance.get(`/tasks-today/${user_id}?group_id=${filter}`)
        .then(response => {
            setTasks(response.data.tasks);
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    const getGroupInfo = async(filter) => {
        if (filter === 0){
            setGroupCount(1);
            return;
        }

        // Sanitize user id
        const user_id = user.sub.split('|')[1].toString();

        axiosInstance.get(`/groups/${filter}`)
        .then(response => {
            setGroupCount(response.data.group.number_of_members);
            setIsOwner(response.data.group.owner === user_id);
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    const addUserToGroup = async (e) => {
        e.preventDefault();

        axiosInstance.get(`/users-by-email/${invite}`)
        .then(response => {
            let user_id = response.data.user.user_id;

            axiosInstance.patch(`/users/${user_id}/groups/${filter}`)
            .then(response => {
                console.log('Group added for new user:', user_id);
                setAdding(false);
            })
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    };

    const deleteGroup = async() => {
        const user_id = user.sub.split('|')[1].toString();
        axiosInstance.delete(`/users/${user_id}/groups/${filter}`)
        .then(response => {
            console.log('Left group');
        })
        .catch(error => {
            console.error('Error leaving group:', error)
        });
    }

    const getCompletionCount = () => {
        const sum = tasks.reduce((total, task) => {
            if (task.members_completion !== null) {
                return total + task.members_completion.split(',').length;
            }
            return total;
          }, 0);

        return sum;
    }

    useEffect(() => {
        if (isAuthenticated && axiosInstance){
            if (lastChecked === -1){
                updateLastChecked();
            }
            getTasks();
            getGroupInfo(filter);
        }
    }, [filter, isAuthenticated, axiosInstance, getGroupInfo, getTasks, lastChecked, updateLastChecked]);

    return (
        isAuthenticated && (
            <div className="TaskPage">
                <Progress checked = {getCompletionCount()} total = {tasks.length * groupCount}/>
                <div className='group-buttons'>
                    {filter !== 0 && isOwner && !adding && <button className="invite-button" onClick={() => setAdding(true)}>Invite</button>}
                    {filter !== 0 && <button className="leave-button" onClick={deleteGroup}>Leave</button>}
                </div>
                <div className='task-view'>
                    {tasks.map((task, index) => (
                        <Task key={task.id} task={task} getTasks={getTasks} groupCount={groupCount}/>
                    ))}
                </div>
                {(filter === 0 || isOwner) && <button className="add-btn" onClick={goToAddPage}>+</button>}
                {isOwner && adding && 
                <div>
                    <input type="text" id="name" onChange={(e) => setInvite(e.target.value)} required/>
                    <button onClick={addUserToGroup}>Add</button>
                </div>}
            </div>
        )
    );
}

export default TaskPage;

import './TaskPage.css';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react";
import Task from '../Components/Task.js';
import Progress from '../Components/Progress.js';
import axios from 'axios';

function TaskPage({ filter }) {
    const [tasks, setTasks] = useState([]);
    const [groupCount, setGroupCount] = useState(0);

    const navigate = useNavigate();

    const goToAddPage = () => {
      navigate('/add');
    };

    const getTasks = async () => {
        //@TODO: modify this to get time update first then patch
        // Get user last checked data
        axios.get(`/users/${1}`)
        .then(response => {
            const today = new Date();
            let pythonEquivalent = (today.getDay() + 6) % 7;
            
            let last_checked = response.data.user.last_checked;
            console.log(last_checked, pythonEquivalent);

            // If mismatch in day reset @TODO: Known bug, same day next week will not reset
            if (last_checked !== pythonEquivalent) {
                console.log("we are resetting");
                axios.patch(`/update-streaks/${1}`)
                .then(response => {
                    console.log('Reset');
                })
                .catch(error => {
                    console.error('There was an error fetching the data:', error);
                });
            }

            // Set last checked time for user    
            axios.patch(`/users/${1}`)
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

        
        // Get todays tasks
        axios.get(`/tasks-today/${1}?group_id=${filter}`)
        .then(response => {
            setTasks(response.data.tasks);
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    const getGroupCount = async(filter) => {
        axios.get(`/groups/${filter}`)
        .then(response => {
            setGroupCount(response.data.group.number_of_members);
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    useEffect(() => {
        getTasks();
        getGroupCount(filter);
    }, [filter]);

    return (
        <div className="TaskPage">
            <Progress checked = {tasks.filter(t => t.complete).length} total = {tasks.length}/>
            {tasks.map((task, index) => (
                <Task key={task.id} task={task} getTasks={getTasks} groupCount={groupCount}/>
            ))}
            <button className="add-btn" onClick={goToAddPage}>+</button>
        </div>
    );
}

export default TaskPage;

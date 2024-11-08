import './TaskPage.css';
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from "react";
import Task from '../Components/Task.js';
import Progress from '../Components/Progress.js';
import axios from 'axios';

function TaskPage() {
    const [tasks, setTasks] = useState([]);

    const navigate = useNavigate();

    const goToAddPage = () => {
      navigate('/add');
    };

    const getTasks = async () => {

        // Set last checked time for user
        axios.patch(`/users/${1}`)
        .then(response => {
            let last_checked = response.data.user.last_checked;
            const today = new Date();
            let pythonEquivalent = (today.getDay() + 6) % 7;
            console.log(last_checked, pythonEquivalent);
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
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
            
        axios.get(`/tasks-today/${1}`)
        .then(response => {
            setTasks(response.data.tasks);
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    useEffect(() => {
        getTasks();
    }, []);

    return (
        <div className="TaskPage">
            <Progress checked = {tasks.filter(t => t.complete).length} total = {tasks.length}/>
            {tasks.map((task, index) => (
                <Task key={task.id} task={task} getTasks={getTasks} />
            ))}
            <button className="add-btn" onClick={goToAddPage}>+</button>
        </div>
    );
}

export default TaskPage;

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
        //@TODO: Change back to /tasks-today
        axios.get('/tasks-today')
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

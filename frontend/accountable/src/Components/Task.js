import './Task.css';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Task(props) {
    let task = props.task;
    let getTasks = props.getTasks;
    let groupCount = props.groupCount;

    const handleDelete = async (id) => {
        axios.delete(`/tasks/${id}`)
        .then(response => {
            console.log('Task data', response.data);
            getTasks();
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    };

    const completeTask = async (id) => {
        const data = {
            "complete": !task.complete,
            "streaks": task.complete? task.streaks - 1 : task.streaks + 1,
            "number_completed": task.complete? task.number_completed - 1 : task.number_completed + 1
        }

        axios.patch(`/tasks/${id}`, data)
        .then(response => {
            console.log('Task data', response.data);
            getTasks();
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    const navigate = useNavigate();

    const handleEdit = async(id) => {
        navigate('/add', { state: { taskId: id } });
    }

    return (
        <div className="task">
            <label className="task-name"><input type="checkbox" checked={task.complete} onChange={() => completeTask(task.id)}/>{task.name}</label>
            <p hidden={!task.shared}>{task.number_completed}/{groupCount}</p>
            <p>{task.streaks}</p>
            <button className='edit-btn' onClick={() => handleEdit(task.id)}>=</button>
            <button className="delete-btn" onClick={() => handleDelete(task.id)}>x</button>
        </div>
    );
}

export default Task;
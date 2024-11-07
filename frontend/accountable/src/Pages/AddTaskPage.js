import './AddTaskPage.css';

import { useEffect, useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

function AddTaskPage() {
    const daysOfTheWeek = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
    const [activeDay, setActiveDay] = useState([false, false, false, false, false, false, false]);
    const [name, setName] = useState("");
    const [frequency, setFrequency] = useState(0);
    const [shared, setShared] = useState(false);

    const navigate = useNavigate();
    const location = useLocation();
    const taskId = location.state?.taskId || null;
    const editOption = Boolean(taskId);

    useEffect(() => {
        if (editOption) {
            axios.get(`/tasks/${taskId}`)
            .then(response => {
                let task = response.data.task;
                let days = Array(7).fill(false);
                for (let i = 0; i < task.days.length; i++){
                    days[parseInt(task.days[i])] = true;
                }

                setName(task.name);
                setFrequency(task.frequency);
                setActiveDay(days);
                setShared(task.shared);
            })
            .catch(error => {
                console.error('There was an error fetching the data:', error);
            });
        }
    }, [taskId, editOption])

    const toggleDay = (index) => {
        setActiveDay((prev) => 
            prev.map((state, i) => (i === index ? !state: state))
        );
    }

    const goToTaskPage = () => {
        navigate('/');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        let days = ""
        activeDay.map((day, index) =>
            day? days += index.toString() : ''
        );

        const data = {
            "name": name,
            "frequency": frequency,
            "days": days,
            "shared": false
        }

        if (editOption){
            axios.patch(`/tasks/${taskId}`, data)
            .then(response => {
                console.log('Task data', response.data);
                navigate('/');
            })
            .catch(error => {
                console.error('There was an error fetching the data:', error);
            });
        } else {
            axios.post('/tasks', data)
            .then(response => {
                console.log('Task data', response.data);
                navigate('/');
            })
            .catch(error => {
                console.log(data);
                console.error('There was an error fetching the data:', error);
            });
        }
    };
        
    return (
        <div>
            <button type="button" onClick={goToTaskPage}>Back</button>

            <form action="/submit" method="POST" onSubmit={handleSubmit}>
                <label>Name:</label>
                <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required/>

                <label>Frequency:</label>
                <input type="number" id="frequency" value={frequency} onChange={(e) => setFrequency(e.target.value)} min="1" max="10" required/>

                <label>Days:</label>
                {activeDay.map((isActive, index) => (
                    <button 
                        type="button" 
                        key={index} 
                        className={`${isActive? 'active' : ''}`} 
                        onClick={() => toggleDay(index)}>
                        {daysOfTheWeek[index]}   
                    </button>
                ))}

                <label> Shared: </label>
                <input type="checkbox" value="no"/>

                <button type="submit" onClick={handleSubmit}>Submit</button>
            </form>
        </div>
    );
}

export default AddTaskPage;

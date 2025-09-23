import { useAuth0 } from '@auth0/auth0-react';
import './Task.css';
import { useNavigate } from 'react-router-dom';
import { useAxios } from '../AxiosInstance';

function Task(props) {
    let task = props.task;
    let getTasks = props.getTasks;
    let groupCount = props.groupCount;

    const { user } = useAuth0();
    const axiosInstance = useAxios();

    const handleDelete = async (id) => {
        axiosInstance.delete(`/tasks/${id}`)
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
            "complete": !inCompletion(),
            "number_completed": inCompletion()? task.number_completed - 1 : task.number_completed + 1,
            "streaks": updateStreaks(),
            "members_completion": inCompletion()? removeCompletion() : addCompletion()
        }

        axiosInstance.patch(`/tasks/${id}`, data)
        .then(response => {
            //console.log('Task data', response.data);
            getTasks();
        })
        .catch(error => {
            console.error('There was an error fetching the data:', error);
        });
    }

    const updateStreaks = () => {
        let streaks = task.streaks;
        if (!inCompletion() && task.number_completed + 1 === groupCount){
            streaks = task.streaks + 1;
        } else if (inCompletion() && task.number_completed === groupCount) {
            streaks = task.streaks - 1;
        }
        return streaks;
    }

    const addCompletion = () => {
        let past = ""
        if (task.members_completion != null){
            past = task.members_completion + ","
        }
        
        return past + user.sub.split('|')[1].toString();
    };

    const removeCompletion = () => {
        if (task.members_completion == null){
            return task.members_completion
        }
        let members_completion = task.members_completion.split(',');
        let arr = members_completion.filter(id => id !== user.sub.split('|')[1].toString());
        if (arr.join(',') === '') return null;
        return arr.join(",");
    }

    const inCompletion = () => {
        if (task.members_completion == null){
            return false;
        }
        let members_completion = task.members_completion.split(',');
        return members_completion.includes(user.sub.split('|')[1].toString());
    }

    const navigate = useNavigate();

    const handleEdit = async(id) => {
        navigate('/add', { state: { taskId: id } });
    }

    return (
        <div className="task">
            <label className="task-name"><input type="checkbox" className="checkbox" checked={inCompletion()} onChange={() => completeTask(task.id)}/>{task.name}</label>
            <div className='end-elements'>
                <p hidden={!task.shared}>{task.number_completed}/{groupCount}</p>
                <p>{task.streaks}🔥</p>
                <button className='edit-btn' onClick={() => handleEdit(task.id)}>=</button>
                <button className="delete-btn" onClick={() => handleDelete(task.id)}>x</button>
            </div>
        </div>
    );
}

export default Task;
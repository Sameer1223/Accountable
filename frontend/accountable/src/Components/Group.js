import './Group.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Group(props) {
    let group = props.group;

    return (
        <div className="group">
            <button className='group-name'>{group}</button>
        </div>
    );
}

export default Group;
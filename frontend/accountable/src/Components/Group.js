import './Group.css';
import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Group(props) {
    let id = props.id;
    let group = props.group;
    let setFilter = props.setFilter;

    return (
        <div className="group">
            <button className='group-name' onClick={()=>setFilter(id)}>{group}</button>
        </div>
    );
}

export default Group;
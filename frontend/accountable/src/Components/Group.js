import './Group.css';
import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Group(props) {
    let id = props.id;
    let group = props.group;
    let setFilter = props.setFilter;
    let count = props.count;

    return (
        <div className="group">
            <button className='group-name-button' onClick={()=>setFilter(id)}>
                <span className='group-name'>{group}</span>
                <span className='group-count'>{count}</span>
            </button>
        </div>
    );
}

export default Group;
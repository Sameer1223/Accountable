import './GroupsView.css';
import axios from 'axios';
import { useEffect, useState } from 'react';
import Group from '../Components/Group.js';

function GroupsView() {  
    const groupNames = ['Individual', 'Group 1', 'Group2'];
    
    return (
        <div className='groups-view'>
            {groupNames.map((group, index) => (
                <Group key={index} group={group} />
            ))}
        </div>
    );
}

export default GroupsView;
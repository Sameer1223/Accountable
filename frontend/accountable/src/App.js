import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TaskPage from './Pages/TaskPage';
import AddTaskPage from './Pages/AddTaskPage';
import GroupsView from './Pages/GroupsView';
import { useState } from 'react';

function App() {
  const [filter, setFilter] = useState(0);

  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div className='main'>
            <GroupsView setFilter={setFilter}/>
            <TaskPage filter={filter}/>
          </div>
        }
        />
        <Route path="/add" element={<AddTaskPage filter={filter}/>} />
      </Routes>
    </Router>
  );
}

export default App;

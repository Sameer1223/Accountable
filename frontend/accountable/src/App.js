import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TaskPage from './Pages/TaskPage';
import AddTaskPage from './Pages/AddTaskPage';
import GroupsView from './Pages/GroupsView';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div className='main'>
            <GroupsView/>
            <TaskPage />
          </div>
        }
        />
        <Route path="/add" element={<AddTaskPage />} />
      </Routes>
    </Router>
  );
}

export default App;

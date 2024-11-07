import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TaskPage from './Pages/TaskPage';
import AddTaskPage from './Pages/AddTaskPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TaskPage />} />
        <Route path="/add" element={<AddTaskPage />} />
      </Routes>
    </Router>
  );
}

export default App;

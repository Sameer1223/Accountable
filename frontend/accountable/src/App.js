//import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Auth0Provider, useAuth0 } from '@auth0/auth0-react';
import TaskPage from './Pages/TaskPage';
import AddTaskPage from './Pages/AddTaskPage';
import GroupsView from './Pages/GroupsView';
import { useState } from 'react';
import AddUser from './Components/AddUser';
import Login from './Components/Login';

const domain = "dev-s266brdcm0m6zmt1.us.auth0.com";
const clientId = "gcE3WcsOMGd4rw8iVGpciqavOYBswzyF";

function App() {
  const [filter, setFilter] = useState(0);
  const { isAuthenticated } = useAuth0();

  return (
    <Auth0Provider
    domain={domain}
    clientId={clientId}
    authorizationParams={{
      redirect_uri: 'http://localhost:3000',
      audience: 'accountable'
    }}>
      <Router>
        <Routes>
          <Route path="/" element={
            <div className='main'>
              <AddUser/>
              <div className='core'>
                <GroupsView setFilter={setFilter}/>
                <TaskPage filter={filter}/>
              </div>
            </div>
          }
          />
          <Route path="/add" element={<AddTaskPage filter={filter}/>} />
        </Routes>
      </Router>
    </Auth0Provider>
  );
}

export default App;

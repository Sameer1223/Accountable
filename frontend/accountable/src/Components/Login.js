import { useNavigate } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';

function Login() {
    const { isAuthenticated, loginWithRedirect, logout } = useAuth0();
    const navigate = useNavigate();

    const handleLogin = () => {
        if (!isAuthenticated){
            //navigate('/login');
            loginWithRedirect();
        } else {
            logout({logoutParams: {returnTo: window.location.origin }})
        }
    };

    return (
        <div>
            <button onClick={handleLogin}>{isAuthenticated ? "Logout" : "Login"}</button>
        </div>
    );
}

export default Login;
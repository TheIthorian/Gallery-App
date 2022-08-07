import Home from './components/home';
import SignIn from './components/sign_in';

import { Route, Routes } from 'react-router-dom';

import './style/header.css';
import './style/style.css';
import './style/popups.css';
import './style/inputs.css';

function App() {
    return (
        <main>
            <Routes>
                <Route
                    exact
                    path='/'
                    element={localStorage.getItem('isLoggedIn') ? <Home /> : <SignIn />}
                />
                <Route path='/sign-in' element={<SignIn />} />
            </Routes>
        </main>
    );
}

export default App;

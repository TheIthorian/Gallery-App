
import Home from './components/home';
import SignIn from './components/sign_in';
//import LogOut from './components/sign_in';

import { Route, Switch } from 'react-router-dom';

import './style/header.css';
import './style/style.css';
import './style/popups.css';

function App() {

    return (
        <main>
            <Switch>
                <Route exact path='/' component={localStorage.getItem('isLoggedIn') ? Home : SignIn} />
                <Route path='/sign-in' component={SignIn} />
            </Switch>
        </main>
    )
}

export default App
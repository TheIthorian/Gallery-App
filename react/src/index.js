import ReactDOM from 'react-dom';

import { BrowserRouter, Route, Switch } from 'react-router-dom';

import App from './app.js'

ReactDOM.render(
    //<Page />,
    <BrowserRouter>
        <App />
    </BrowserRouter>,
    document.getElementById('root')
);
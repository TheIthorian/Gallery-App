import ReactDOM from 'react-dom';

import { BrowserRouter, Route, Switch } from 'react-router-dom';

import App from './app.js'

import "./style/root.css";
import "./style/buttons.css";
import "./style/inputs.css";
import "./style/scroll.css";

ReactDOM.render(
    //<Page />,
    <BrowserRouter>
        <App />
    </BrowserRouter>,
    document.getElementById('root')
);
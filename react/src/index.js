import ReactDOM from 'react-dom';

import { BrowserRouter } from 'react-router-dom';

import App from './app.js';

import './style/root.css';
import './style/buttons.css';
import './style/inputs.css';
import './style/scroll.css';

ReactDOM.render(
    <BrowserRouter>
        <App />
    </BrowserRouter>,
    document.getElementById('root')
);

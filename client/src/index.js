import axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { HOST_ADDR } from './consts';
import './index.css';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

axios.post(HOST_ADDR + '/api/auth_check/').then(() => {
	ReactDOM.render(<App loggedIn={true}/>, document.getElementById('root'));
	registerServiceWorker();
}).catch((error) => {
	if (error.response.status < 500) {
		ReactDOM.render(<App loggedIn={false}/>, document.getElementById('root'));
	}
	registerServiceWorker();
});

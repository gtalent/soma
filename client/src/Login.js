import axios from 'axios';
import React from 'react';
import { HOST_ADDR } from './consts';
import Button from '@material-ui/core/Button';
import {
	Divider,
	Paper,
	TextField,
} from '@material-ui/core';


class Login extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
			email: '',
			password: '',
		};
	}

	handleEmailChange = (event) => {
		this.setState({
			email: event.target.value,
		});
	};

	handlePasswordChange = (event) => {
		this.setState({
			password: event.target.value,
		});
	};

	loginClick = (event) => {
		axios.post(HOST_ADDR + '/api/authenticate/', {
			username: this.state.email,
			password: this.state.password,
		}).then(function(response) {
			if (response.status === 200) {
				window.location.reload();
			}
		});
	};

	render() {
		const style = {
			height: 137,
			width: 325,
			display: 'inline-block',
		};
		return (
			<div style={{textAlign: 'center'}}>
				<Paper style={style}>
					<TextField label='Email'
								  onChange={this.handleEmailChange}
					/>
					<Divider/>
					<TextField label='Password'
					           type='password'
								  onChange={this.handlePasswordChange}
					/>
					<Divider/>
					<Button raised='true'
					              style={{width: style.width * 0.75}}
									  color='primary'
					              onClick={this.loginClick}
					>
						 Sign In
					</Button>
				</Paper>
			</div>
		);
	}

};

export default Login

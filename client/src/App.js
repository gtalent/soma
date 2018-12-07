
import React from 'react';
import {
	BrowserRouter as Router,
	Redirect,
	Route,
} from 'react-router-dom';
import { createMuiTheme } from '@material-ui/core/styles';
import {
	MuiThemeProvider,
	Toolbar,
} from '@material-ui/core';
import './App.css';
import Directory from './Directory';
import PersonEdit from './PersonEdit';
import PersonView from './PersonView';
import Login from './Login';


class App extends React.Component {

	constructor(props) {
		super(props);
		this.state = {loggedIn: props.loggedIn};
	}

	render() {
		let appRoot = null;
		if (this.state.loggedIn) {
			appRoot = (
				<div>
					<Toolbar/>
					<Route exact path='/' render={() => (
						<Redirect to="/church_directory/page/0/"/>
					)}/>
					<Route path='/church_directory/page/' component={() => (
						<div>
							<Directory membershipStatus={
									[
										'Member',
									]
								}
							/>
						</div>
					)}/>
					<Route path='/person/view/:personId/' component={({match}) => (
						<div>
							<PersonView personId={parseInt(match.params.personId, 10)}/>
						</div>
					)}/>
					<Route path='/person/edit/:personId/' component={({match}) => (
						<div>
							<PersonEdit personId={parseInt(match.params.personId, 10)}/>
						</div>
					)}/>
				</div>
			);
		} else {
			appRoot = <Login/>;
		}
		return (
			<Router>
				<div>
					{appRoot}
				</div>
			</Router>
		);
	}
};

export default App;


import React from 'react';
import {
	BrowserRouter as Router,
	Redirect,
	Route,
} from 'react-router-dom';
import theme from 'material-ui/styles/baseThemes/lightBaseTheme';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {
	MuiThemeProvider,
} from 'material-ui';
import './App.css';
import Directory from './Directory';
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
					<Route exact path='/' render={() => (
						<Redirect to="/church_directory/page/0/"/>
					)}/>
					<Route path='/church_directory/page/' render={() => (
						<div>
							<Directory membershipStatus={
									[
										'Active Member',
										'Homebound Member',
										'Out-of-area Member',
									]
								}
							/>
						</div>
					)}/>
					<Route path='/person/:personId/' component={({match}) => (
						<div>
							<PersonView personId={parseInt(match.params.personId, 10)}/>
						</div>
					)}/>
				</div>
			);
		} else {
			appRoot = <Login/>;
		}
		return (
			<Router>
				<MuiThemeProvider muiTheme={getMuiTheme(theme)}>
					<div>
						{appRoot}
					</div>
				</MuiThemeProvider>
			</Router>
		);
	}
};

export default App;

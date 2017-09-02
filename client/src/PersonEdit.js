
import axios from 'axios';
import React from 'react';
import Button from 'material-ui/Button';
import Table, {
	TableBody,
	TableCell,
	TableRow,
} from 'material-ui/Table';
import TextField from 'material-ui/TextField';
import { HOST_ADDR } from './consts';

class PersonEdit extends React.Component {

	constructor(props) {
		super(props);
		this.state = {personId: props.personId, person: {}};
		this.cancelTokens = [];
	}

	buildElements = (o) => {
		if (typeof(o) === 'object') {
			let out = [];
			let key = 1;
			for (let i in o) {
				let v = o[i];
				out.push(<div key={key++}>{v}</div>);
			}
			return out;
		} else {
			return o;
		}
	};

	componentDidMount(prevProps, prevState) {
		let dir = this;
		let ct = axios.CancelToken.source();
		axios.post(HOST_ADDR + '/api/church_directory/person/', {
			person_id: this.state.personId,
		},
		{
			cancelToken: ct.token,
		}).then((response) => {
			if (response.status === 200) {
				dir.setState({person: response.data});
				for (let i in dir.cancelTokens) {
					dir.cancelTokens.splice(i, 1);
				}
			}
		}).catch((thrown) => {
		});
		this.cancelTokens.push(ct);
	}

	componentWillUnmount(prevProps, prevState) {
		for (let i in this.cancelTokens) {
			this.cancelTokens[i].cancel();
		}
		this.cancelTokens = [];
	}

	createTextField = (name, valName) => (
		<TextField
			label={name}
			value={this.state.person[valName] || ''}
			style={{marginLeft: 10}}
			onChange={event => {
				let s = this.state;
				s.person[valName] = event.target.value;
				this.setState(s);
			}}
		/>
	);

	createDateField = (name, valName) => (
		<TextField
			type='date'
			label={name}
			value={this.state.person[valName] || ''}
			style={{marginLeft: 10}}
			onChange={event => {
				let s = this.state;
				s.person[valName] = event.target.value;
				this.setState(s);
			}}
		/>
	);

	emailBtn = (name, val) => {
		window.location.href = 'mailto:' + this.state.person.email_address;
	};

	cellPhoneBtn = (name, val) => {
		window.location.href = 'tel:+1' + this.state.person.cell_number;
	};

	homePhoneBtn = (name, val) => {
		window.location.href = 'tel:+1' + this.state.person.home_number;
	};

	render() {
		let p = this.state.person;
		return (
			<div style={{maxWidth: '900px', margin: '0 auto', display: 'flex'}}>
				<div style={{minWidth: '350px'}}>
					{
						p.image_url ? (
							<img
								src={'/api/' + p.image_url}
								alt={p.first_name + ' ' + p.last_name}
								width='97%'
							/>
						) : null
					}
				</div>
				<div style={{minWidth: '350px'}}>
					<div>
						<Button raised disabled style={{margin: 5}} color='primary'>
							Save
						</Button>
					</div>
					<Table>
						<TableBody>
							<TableRow>
								<TableCell>Basic Info</TableCell>
								<TableCell>
									<div>
										{this.createTextField('First Name', 'first_name')}
										{this.createTextField('Last Name', 'last_name')}
									</div>
									<div>{this.createDateField('Birthday', 'birthday')}</div>
								</TableCell>
							</TableRow>
							<TableRow>
								<TableCell>Contact</TableCell>
								<TableCell>
									<div>
										{this.createTextField('Home Phone', 'home_number')}
										{this.createTextField('Cell Phone', 'cell_number')}
									</div>
									{this.createTextField('Address Line 1', 'address_line1')}
									{this.createTextField('Address Line 2', 'address_line2')}
									<div>{this.createTextField('Email', 'email_address')}</div>
								</TableCell>
							</TableRow>
						</TableBody>
					</Table>
				</div>
			</div>
		);
	}

};

export default PersonEdit;

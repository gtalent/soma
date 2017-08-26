
import axios from 'axios';
import React from 'react';
import {
	RaisedButton,
	Table,
	TableBody,
	TableRow,
	TableRowColumn,
} from 'material-ui';
import { HOST_ADDR } from './consts';

class PersonView extends React.Component {

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

	buildRow = (name, value) => {
		return value ? (
			<TableRow>
				<TableRowColumn>{name}</TableRowColumn>
				<TableRowColumn>{this.buildElements(value)}</TableRowColumn>
			</TableRow>
		) : null;
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
		for (var i in this.cancelTokens) {
			this.cancelTokens[i].cancel();
		}
		this.cancelTokens = [];
	}

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
		let btnStyle = {margin: 5};
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
					<RaisedButton style={btnStyle} onClick={this.cellPhoneBtn} label='Call Cell' disabled={!p.cell_number}/>
					<RaisedButton style={btnStyle} onClick={this.homePhoneBtn} label='Call Home' disabled={!p.home_number}/>
					<RaisedButton style={btnStyle} onClick={this.emailBtn} label='Email' disabled={!p.email_address}/>
					<RaisedButton style={btnStyle} label='Edit' secondary={true}/>
					<Table selectable={false}>
						<TableBody displayRowCheckbox={false}>
							{this.buildRow('Name', p.first_name + ' ' + p.last_name)}
							{this.buildRow('Home Phone', p.home_number)}
							{this.buildRow('Cell Phone', p.cell_number)}
							{this.buildRow('Email', p.email_address)}
							{this.buildRow('Address', p.address)}
						</TableBody>
					</Table>
				</div>
			</div>
		);
	}

};

export default PersonView;

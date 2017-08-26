
import axios from 'axios';
import React from 'react';
import {
	Redirect,
	Route,
} from 'react-router-dom';
import Button from 'material-ui/Button';
import Card, {
	CardActions,
	CardContent,
	CardHeader,
} from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import ExpandMoreIcon from 'material-ui-icons/ExpandMore';
import Collapse from 'material-ui/transitions/Collapse';
import {
	Divider,
} from 'material-ui';
import { HOST_ADDR } from './consts';

const ENTRIES_PER_PAGE = 5;

class DirectoryEntry extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			expanded: false,
			personId: props.personId,
			name: props.name,
			membershipStatus: props.membershipStatus,
			addressLine1: props.addressLine1,
			addressLine2: props.addressLine2,
			cellNumber: props.cellNumber,
			homeNumber: props.homeNumber,
			emailAddress: props.emailAddress,
		};
	}

	field = (name, val) => {
		if (val) {
			return (
				<div>
					{name}: {val}
				</div>
			);
		}
	}

	emailBtn = (name, val) => {
		window.location.href = 'mailto:' + this.state.emailAddress;
	};

	cellPhoneBtn = (name, val) => {
		window.location.href = 'tel:+1' + this.state.cellNumber;
	};

	homePhoneBtn = (name, val) => {
		window.location.href = 'tel:+1' + this.state.homeNumber;
	};

	render() {
		return (
			<div>
				<Card>
					<CardHeader
						title={this.state.name}
						subheader={this.state.membershipStatus}
					/>
					<CardActions disableActionSpacing>
						<Button onClick={this.cellPhoneBtn} disabled={!this.state.cellNumber}>
							Call Cell
						</Button>
						<Button onClick={this.homePhoneBtn} disabled={!this.state.homeNumber}>
							Call Home
						</Button>
						<Button onClick={this.emailBtn} disabled={!this.state.emailAddress}>
							Email
						</Button>
						<Button color='primary' href={'/person/' + this.state.personId + '/'}>
							View
						</Button>
						<Button color='accent'>
							Edit
						</Button>
						<div style={{flex: '1 1 auto'}}/>
						<IconButton
							onClick={() => this.setState({expanded: !this.state.expanded})}
							aria-expanded={this.state.expanded}
							aria-label="Show more"
						>
							<ExpandMoreIcon/>
						</IconButton>
					</CardActions>
					<Collapse in={this.state.expanded} transitionDuration="auto" unmountOnExit>
						<CardContent>
							{this.state.addressLine1}
							<br/>
							{this.state.addressLine2}
							<Divider/>
							{this.field('Cell', this.state.cellNumber)}
							{this.field('Home', this.state.homeNumber)}
							{this.field('Email', this.state.emailAddress)}
						</CardContent>
					</Collapse>
				</Card>
			</div>
		);
	}

};

class DirectoryPage extends React.Component {

	constructor(props) {
		super(props);

		this.state = {};
		this.cancelTokens = [];
	}

	componentDidMount(prevProps, prevState) {
		let props = this.props;
		let pageStart = props.page * ENTRIES_PER_PAGE;
		let dir = this;
		let ct = axios.CancelToken.source();
		axios.post(HOST_ADDR + '/api/church_directory/directory_page/', {
			membership_status: props.membershipStatus,
			start: pageStart,
			end: pageStart + ENTRIES_PER_PAGE,
		},
		{
			cancelToken: ct.token,
		}).then(function(response) {
			if (response.status === 200) {
				dir.setState({people: response.data, page: props.page});
				for (var i in dir.cancelTokens) {
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

	render() {
		let cards = [];
		for (let i in this.state.people) {
			let m = this.state.people[i];
			let id = (i + 1) * (this.state.page + 1);
			cards.push(
				<DirectoryEntry
					key={id}
					personId={m.person_id}
					name={m.last_name + ', ' + m.first_name}
					membershipStatus={m.membership_status}
					addressLine1={m.address.address_line1}
					addressLine2={m.address.address_line2}
					cellNumber={m.cell_number}
					homeNumber={m.home_number}
					emailAddress={m.email_address}
				/>
			);
			cards.push(<br key={id + this.state.people.length}/>);
		}
		return (
			<div>
				{cards}
			</div>
		);
	}

};

class Directory extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
			membershipStatus: props.membershipStatus,
			state: 0,
			page: 0,
			pages: 1,
		};

		let dir = this;
		axios.post(HOST_ADDR + '/api/church_directory/group_stat/', {
			membership_status: props.membershipStatus
		}).then(function(response) {
			if (response.status === 200) {
				let groupSize = response.data.group_size;
				dir.setState({
					pages: Math.floor(groupSize / ENTRIES_PER_PAGE),
				});
			}
		});
	}

	updatePage = (p) => {
		this.setState({page: p});
		this.redirect = '/church_directory/page/' + p + '/';
	};

	render() {
		let btnStyle = {margin: 20};
		if (this.redirect) {
			let r = this.redirect;
			this.redirect = undefined;
			return (
				<Redirect to={r}/>
			);
		} else {
			return (
				<div>
					<Route exact path='/church_directory/page/' component={() => (
						<Redirect to="/church_directory/page/0/"/>
					)}/>
					<Route path='/church_directory/page/:page/' component={({match}) => {
						let page = parseInt(match.params.page, 10);
						return (
							<div style={{maxWidth: '700px', margin: '0 auto'}}>
								<div style={{display: 'flex', justifyContent: 'center'}}>
									<Button raised
										style={btnStyle}
										color='primary'
										disabled={page < 1}
										onClick={(event) => this.updatePage(page - 1)}
									>
										Prev
									</Button>
									<Button raised
										style={btnStyle}
										color='primary'
										disabled={page >= this.state.pages}
										onClick={(event) => this.updatePage(page + 1)}
									>
										Next
									</Button>
								</div>
								<DirectoryPage
									membershipStatus={this.state.membershipStatus}
									page={page}
								/>
							</div>
						);
					}}/>
				</div>
			);
		}
	}

};

export default Directory;

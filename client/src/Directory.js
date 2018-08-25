
import axios from 'axios';
import React from 'react';
import {
	Link,
	Redirect,
	Route,
} from 'react-router-dom';
import Avatar from 'material-ui/Avatar';
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

const ENTRIES_PER_PAGE = 25;

class DirectoryEntry extends React.Component {

	constructor(props) {
		super(props);
		let msMod = '';
		if (props.outOfArea) {
			msMod = ' - Out-of-Area';
		} else if (props.homebound) {
			msMod = ' - Homebound';
		}
		this.state = {
			expanded: false,
			personId: props.personId,
			name: props.name,
			membershipStatus: props.membershipStatus + msMod,
			addressLine1: props.addressLine1,
			addressLine2: props.addressLine2,
			city: props.city,
			province: props.province,
			cellNumber: props.cellNumber,
			homeNumber: props.homeNumber,
			emailAddress: props.emailAddress,
			imageUrl: props.imageUrl,
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

	namelessField = (val) => {
		if (val) {
			return (
				<div>
					{val}
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
						avatar={
							this.state.imageUrl ? <Avatar
								src={'/api/' + this.state.imageUrl}
							/> : null
						}
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
						<Button
							color='primary'
							component={Link}
							to={'/person/view/' + this.state.personId + '/'}
						>
							View
						</Button>
						<Button
							color='accent'
							component={Link}
							to={'/person/edit/' + this.state.personId + '/'}
						>
							Edit
						</Button>
						<div style={{flex: '1 1 auto'}}/>
						<IconButton
							onClick={() => this.setState({expanded: !this.state.expanded})}
							aria-expanded={this.state.expanded}
							aria-label='Show more'
						>
							<ExpandMoreIcon/>
						</IconButton>
					</CardActions>
					<Collapse in={this.state.expanded} transitionDuration='auto' unmountOnExit>
						<CardContent>
							{this.namelessField(this.state.addressLine1)}
							{this.namelessField(this.state.addressLine2)}
							{this.namelessField([this.state.city, this.state.province].join(', '))}
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
				dir.cancelTokens.splice(dir.cancelTokens.indexOf(ct), 1);
			}
		}).catch((thrown) => {
		});
		this.cancelTokens.push(ct);
	}

	componentWillUnmount(prevProps, prevState) {
		for (let v of this.cancelTokens) {
			v.cancel();
		}
		this.cancelTokens = [];
	}

	render() {
		let cards = [];
		for (let i in this.state.people) {
			let m = this.state.people[i];
			cards.push(
				<DirectoryEntry
					key={m.person_id}
					personId={m.person_id}
					name={m.last_name + ', ' + m.first_name}
					membershipStatus={m.membership_status}
					homebound={m.homebound}
					outOfArea={m.out_of_area}
					addressLine1={m.address_line1}
					addressLine2={m.address_line2}
					city={m.city}
					province={m.province}
					cellNumber={m.cell_number}
					homeNumber={m.home_number}
					emailAddress={m.email_address}
					imageUrl={m.image_url}
				/>
			);
			cards.push(<br key={m.person_id + 0.5}/>);
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

	render() {
		let btnStyle = {margin: 20};
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
									component={Link}
									to={'/church_directory/page/' + (page - 1) + '/'}
								>
									Prev
								</Button>
								<Button raised
									style={btnStyle}
									color='primary'
									disabled={page >= this.state.pages}
									component={Link}
									to={'/church_directory/page/' + (page + 1) + '/'}
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

};

export default Directory;

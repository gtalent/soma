//import path from 'path';
//import Express from 'express';
//import React from 'react';
//import { createStore } from 'redux';
//import { Provider } from 'react-redux';
//import { renderToString } from 'react-dom/server'
//import counterApp from './reducers';
//import App from './App';
//
//const app = Express();
//const port = 3000;
//
////Serve static files
//app.use('/static', Express.static('static'));
//
//// This is fired every time the server side receives a request
//app.use((req, res) => {
//	// Render the component to a string
//	const html = renderToString(
//		<App/>
//	)
//
//	// Send the rendered page back to the client
//	res.send(renderFullPage(html))
//});
//
//// We are going to fill these out in the sections to follow
//function renderFullPage(html) {
//  return `
//		<!doctype html>
//		<html>
//			<head>
//				<meta charset="utf-8">
//				<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
//				<meta name="theme-color" content="#000000">
//				<link rel="manifest" href="%PUBLIC_URL%/manifest.json">
//				<link rel="shortcut icon" href="%PUBLIC_URL%/favicon.ico">
//				<title>Church Directory</title>
//			</head>
//			<body>
//				<noscript>
//					You need to enable JavaScript to run this app.
//				</noscript>
//				<div id="root">${html}</div>
//				<script src="/static/bundle.js"></script>
//			</body>
//		</html>
//    `;
//}
//
//app.listen(port)

const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'build')));

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(3000);

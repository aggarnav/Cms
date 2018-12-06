var exec = require('child_process').exec;
var express = require("express");
var fs = require('fs'); 
var app = express();
var bodyParser = require('body-parser')

// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())


app.post('/route', function(req,res){
	body=req.body;
	console.log(body);
	if (body.type=='circle'){
		exec("python cms.py -circle");
		return;
	};
	if (body.circler){
		exec("python cms.py -circle -radius "+ body.circler);
				return;

	};
	if (body.type=='img'){
		exec("python cms.py -image");
		return;

	};
	if (body.type=='bubble'){
		exec("python cms.py -bubble");
		return;

	};
	if (body.bubblel){
		console.log("python cms.py -bubble -labelForBubble \""+body.bubblel+"\"");
		exec("python cms.py -bubble -labelForBubble \""+body.bubblel+"\"");
		return;

		};
	if (body.type=='bubblei'){
		exec("python cms.py -bubble -imgForBubble");
		return;

		};
	if (body.type=='square'){
		exec("python cms.py -square");
		return;

		};
	if (body.type=='triangle'){
		exec("python cms.py -triangle");
		return;

		};	
});
app.get('/', function(req, res){
    res.sendFile('/index.html', {root: __dirname })});
app.listen(4000);
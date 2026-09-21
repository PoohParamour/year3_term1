var
	MW = require("./libs/mw.js"),
	EXPRESS = require("express"),
	APP = EXPRESS(),
	PROTECTED_APP = EXPRESS.Router(),
	PORT_INT = Number(process.env.PORT_STR) || 8080,
	CORS = require("cors");
	
APP.use(CORS({
	credentials: true // for authorization
}));


//Our middleware that authenticates all APIs under our 'authenticatedRoute' Router
//MW.protectThisGetResource
// 

APP.post("/sightings", MW.protectThisGetResource, MW.getSightings, function(req, res, next){
	res.status(200).send({
		cognito_username_str: req.cognito_username_str,
		sightings_obj_arr: req.sightings_obj_arr
	});
});
APP.post("/report-sightings", MW.protectThisGetResource, function(req, res, next){
	//console.log(req.headers);
	res.status(200).send({
		cognito_username_str: req.cognito_username_str
	});
});
APP.post("/siteadmin", MW.protectThisGetResource, function(req, res, next){
	//console.log(req.headers);
	res.status(200).send({
		cognito_username_str: req.cognito_username_str
	});
});




APP.listen(PORT_INT, function(){console.log("Live on port: " + PORT_INT.toString());});
/*
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

/*
Copyright @2021 [Amazon Web Services] [AWS]
    
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

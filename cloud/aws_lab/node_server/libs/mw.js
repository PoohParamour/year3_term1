var MW = (function(){

	//TEMP
	
    var 
        expose = {
            getSightings,
            protectThisGetResource
        };

	var 
        STUDENT_INFO_OBJ_ARR = require("./student_info.json"),
		COGNITO_EXPRESS = require("cognito-express"),
		COGNITO_EXPRESS_SESSION = new COGNITO_EXPRESS({
			region: process.env.REGION_STR || "us-east-1",
			cognitoUserPoolId: process.env.USER_POOL_ID_STR,
			tokenUse: "id",
			tokenExpiration: Number(process.env.TIMEOUT_STR) || 3600 * 1000 //Up to default expiration of 1 hour (3600000 ms)
		}),
		AWS = require("aws-sdk");


	function protectThisGetResource(req, res, next){
		var access_token_str = "";
		// req.query
		if(req.headers && req.headers.authorization){

			var id_str = req.headers.authorization.replace("Bearer ", "");
			console.log(id_str);
			COGNITO_EXPRESS_SESSION.validate(id_str, function(err, response) {
				if(err){
					console.log("Problem with validation at cognito", err);
					return res.status(403).send({
						//cold use HTML (template etc) if this is a GET vs POST
						msg_str: "Sorry you that token is not valid" + err
					});
				}
				// 
			

				console.log("OK login response", response);
				//still here we are golden
				if (response["cognito:groups"] =="Administrators"){
					req.cognito_username_str = response["cognito:username"];
					req.cognito_username_str +='-';
					req.cognito_username_str += response["cognito:groups"];
				} else {
					req.cognito_username_str = response["cognito:username"];
				}
				next();
				console.log(req.cognito_username_str);
			});
		}else{
			return res.status(403).send({
				//cold use HTML (template etc) if this is a GET vs POST
				msg_str: "Sorry you need to pass authenticated headers"
			});
		}
	}

	async function getSightings(req, res, next){
		console.log("Get hard coded sightings from JSON file.");
		req.sightings_obj_arr = STUDENT_INFO_OBJ_ARR.slice();
        next();
    }

	return expose;
   

})();
module.exports = MW;

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

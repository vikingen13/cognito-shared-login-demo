DeployUserPool:
	cd shared-cognito-userpool/;cdk deploy --outputs-file ./cdk-outputs.json

CreateCognitoConf:
	cd common; python populateConfigFile.py

PushFiles:
	rm -rf .git/
	cd app1/;git init;git remote add origin codecommit://CognitoApp1;git add .;git commit -m "initial revision";git push -u origin master
	cd app2/;git init;git remote add origin codecommit://CognitoApp2;git add .;git commit -m "initial revision";git push -u origin master


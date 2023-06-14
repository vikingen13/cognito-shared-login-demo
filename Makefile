COGNITODOMAIN=shareduserpool123456

BuildEnv:
	cd shared-cognito-userpool/;python3 -m venv ./.venv;source .venv/bin/activate;pip install -r requirements.txt

DeployUserPool:
	cd shared-cognito-userpool/;source .venv/bin/activate;cdk deploy --parameters cognitoDomain=$(COGNITODOMAIN) --require-approval never --outputs-file ./cdk-outputs.json

CreateCognitoConf:
	cd common; python3 populateConfigFile.py

PushFiles:
	rm -rf .git/
	cd app1/;git init;git remote add origin codecommit://CognitoApp1;git add .;git commit -m "initial revision";git push -u origin master
	cd app2/;git init;git remote add origin codecommit://CognitoApp2;git add .;git commit -m "initial revision";git push -u origin master

all: BuildEnv DeployUserPool CreateCognitoConf PushFiles

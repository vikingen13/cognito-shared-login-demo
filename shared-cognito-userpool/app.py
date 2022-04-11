#!/usr/bin/env python3

import aws_cdk as cdk

from shared_cognito_userpool.shared_cognito_userpool_stack import SharedCognitoUserpoolStack


app = cdk.App()
SharedCognitoUserpoolStack(app, "shared-cognito-userpool")

app.synth()

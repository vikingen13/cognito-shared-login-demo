const cognitoconf ={
    "federationTarget": "COGNITO_USER_POOLS", 
    "aws_cognito_mfa_types": [
        "SMS"
    ], 
    "aws_cognito_username_attributes": [], 
    "aws_project_region": "eu-west-1", 
    "aws_cognito_social_providers": [], 
    "aws_cognito_password_protection_settings": {
        "passwordPolicyMinLength": 8, 
        "passwordPolicyCharacters": []
    }, 
    "aws_cognito_region": "eu-west-1", 
    "aws_cognito_signup_attributes": [], 
    "aws_user_pools_id": "eu-west-1_Bupz1zZqm", 
    "oauth": {
        "redirectSignIn": "http://localhost:3000/,https://master.d18wek4gy26kwp.amplifyapp.com/", 
        "scope": [
            "phone", 
            "email", 
            "openid", 
            "profile", 
            "aws.cognito.signin.user.admin"
        ], 
        "domain": "sharedpool21321.auth.eu-west-1.amazoncognito.com", 
        "redirectSignOut": "http://localhost:3000/,https://master.d18wek4gy26kwp.amplifyapp.com/", 
        "responseType": "code"
    }, 
    "aws_user_pools_web_client_id": "4fp59ous4saag3fvatnu0olft7", 
    "aws_cognito_verification_mechanisms": [
        "EMAIL"
    ], 
    "aws_cognito_mfa_configuration": "OFF"
} ;

export default cognitoconf;
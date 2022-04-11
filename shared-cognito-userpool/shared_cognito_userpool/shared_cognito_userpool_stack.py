from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_cognito as cognito,
    aws_codecommit as codecommit,
    aws_amplify_alpha as amplify,
    CfnOutput
)


class SharedCognitoUserpoolStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        myPool = cognito.UserPool(self, "shared-cognito-userpool",self_sign_up_enabled=True,
        sign_in_aliases=cognito.SignInAliases(
            username=False,
            email=True
        ),
            password_policy=cognito.PasswordPolicy(
        min_length=8,
        require_lowercase=False,
        require_uppercase=False,
        require_digits=False,
        require_symbols=False,
        temp_password_validity=Duration.days(3))
        )

        myDomain = myPool.add_domain("CognitoDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="sharedpool21321"
            )
        )

        myRepoApp1 = codecommit.Repository(self, "Repository1",
            repository_name="CognitoApp1",
            description="This is a repository for CognitoApp1"
        )

        myRepoApp2 = codecommit.Repository(self, "Repository2",
            repository_name="CognitoApp2",
            description="This is a repository for CognitoApp2"
        )


        myAmplifyApp1 = amplify.App(self, "CognitoApp1",
           source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=myRepoApp1)
        )

        myMaster1 = myAmplifyApp1.add_branch("master") # `id` will be used as repo branch name


        myAmplifyApp2 = amplify.App(self, "CognitoApp2",
           source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=myRepoApp2)
        )

        myMaster2 = myAmplifyApp2.add_branch("master") # `id` will be used as repo branch name

        myApp1 = myPool.add_client("app1",
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True
                ),
                scopes=[cognito.OAuthScope.OPENID,cognito.OAuthScope.EMAIL,cognito.OAuthScope.COGNITO_ADMIN,cognito.OAuthScope.PHONE,cognito.OAuthScope.PROFILE],
                callback_urls=["http://localhost:3000/","https://master.{}/".format(myAmplifyApp1.default_domain)],
                logout_urls=["http://localhost:3000/","https://master.{}/".format(myAmplifyApp1.default_domain)]
        ))

        myApp2 = myPool.add_client("app2",
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True
                ),
                scopes=[cognito.OAuthScope.OPENID,cognito.OAuthScope.EMAIL,cognito.OAuthScope.COGNITO_ADMIN,cognito.OAuthScope.PHONE,cognito.OAuthScope.PROFILE],
                callback_urls=["http://localhost:3000/","https://master.{}/".format(myAmplifyApp2.default_domain)],
                logout_urls=["http://localhost:3000/","https://master.{}/".format(myAmplifyApp2.default_domain)]
        ))

        #last we write the output
        CfnOutput(self, "UserPoolId", value=myPool.user_pool_id)
        CfnOutput(self, "UserPoolApp1Id", value=myApp1.user_pool_client_id)
        CfnOutput(self, "UserPoolApp2Id", value=myApp2.user_pool_client_id)
        CfnOutput(self, "UserPoolDomain", value=myDomain.base_url())
        CfnOutput(self, "App1Domain", value=myAmplifyApp1.default_domain)
        CfnOutput(self, "App2Domain", value=myAmplifyApp2.default_domain)



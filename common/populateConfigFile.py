import json
import copy

def replaceValues(anOriginalDict, aUserPoolId, aDomain, anAppId,anAppDomain):
    myModifiedDict = copy.deepcopy(anOriginalDict)
    myModifiedDict["aws_user_pools_id"] = aUserPoolId
    myModifiedDict["aws_user_pools_web_client_id"]=anAppId
    myModifiedDict["oauth"]["domain"]=aDomain
    myModifiedDict["oauth"]["redirectSignIn"]="{},https://master.{}/".format(myModifiedDict["oauth"]["redirectSignIn"],anAppDomain)
    myModifiedDict["oauth"]["redirectSignOut"]="{},https://master.{}/".format(myModifiedDict["oauth"]["redirectSignOut"],anAppDomain) 
    return myModifiedDict


if __name__ == '__main__':
    print("loading the output file")
    with open("../shared-cognito-userpool/cdk-outputs.json","r") as myOutputFile:
        myOutput = json.load(myOutputFile)

    myUserPoolDomain = myOutput['shared-cognito-userpool']['UserPoolDomain'].replace("https://","")
    myUserPoolId = myOutput['shared-cognito-userpool']['UserPoolId']
    myUserPoolApp1Id = myOutput['shared-cognito-userpool']['UserPoolApp1Id']
    myApp1Domain = myOutput['shared-cognito-userpool']['App1Domain']
    myUserPoolApp2Id = myOutput['shared-cognito-userpool']['UserPoolApp2Id']
    myApp2Domain = myOutput['shared-cognito-userpool']['App2Domain']
    
    #then we load the generic file
    print("loading the generic file")
    with open("cognitoConf.json","r") as myGenericFile:
        myGeneric = json.load(myGenericFile)

    #we create the first file
    myModifiedJson1 = replaceValues(myGeneric,myUserPoolId,myUserPoolDomain,myUserPoolApp1Id,myApp1Domain)

    with open("../app1/src/cognitoConf.js","w") as myConfigFile:
        myConfigFile.write("const cognitoconf ={} ;\n\nexport default cognitoconf;".format(myModifiedJson1))


    #we create the second file
    myModifiedJson2 = replaceValues(myGeneric,myUserPoolId,myUserPoolDomain,myUserPoolApp2Id,myApp2Domain)
    with open("../app2/src/cognitoConf.js","w") as myConfigFile:
        myConfigFile.write("const cognitoconf ={} ;\n\nexport default cognitoconf;".format(myModifiedJson2))


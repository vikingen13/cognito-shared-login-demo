import React, { useEffect, useState } from 'react';
import Amplify, { Auth, Hub } from 'aws-amplify';
import cognitoConf from './cognitoConf';


const isLocalhost = Boolean(
    window.location.hostname === "localhost" ||
      // [::1] is the IPv6 localhost address.
      window.location.hostname === "[::1]" ||
      // 127.0.0.1/8 is considered localhost for IPv4.
      window.location.hostname.match(
        /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/
      )
  );
  
  // Assuming you have two redirect URIs, and the first is for localhost and second is for production
  const [
    localRedirectSignIn,
    productionRedirectSignIn,
  ] = cognitoConf.oauth.redirectSignIn.split(",");
  
  const [
    localRedirectSignOut,
    productionRedirectSignOut,
  ] = cognitoConf.oauth.redirectSignOut.split(",");
  
  const updatedAwsConfig = {
    ...cognitoConf,
    oauth: {
      ...cognitoConf.oauth,
      redirectSignIn: isLocalhost ? localRedirectSignIn : productionRedirectSignIn,
      redirectSignOut: isLocalhost ? localRedirectSignOut : productionRedirectSignOut,
    }
  }
  
console.log(updatedAwsConfig);
console.log(cognitoConf.oauth.redirectSignIn);
Amplify.configure(updatedAwsConfig);

//Amplify.configure(awsconfig);

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    Auth.currentAuthenticatedUser()
    .then(user => setUser(user))
    .catch(err => Auth.federatedSignIn());

    if(user || window.location.search != ""){

        Hub.listen('auth', ({ payload: { event, data } }) => {
        switch (event) {
            case 'signIn':
            case 'cognitoHostedUI':
            getUser().then(userData => setUser(userData));
            break;
            case 'signOut':
            setUser(null);          
            break;
            case 'signIn_failure':
            case 'cognitoHostedUI_failure':
            console.log('Sign in failure', data);
            break;
        }
        });

    }else{
        Auth.federatedSignIn();
    }
    getUser().then(userData => setUser(userData));
  }, []);

  function getUser() {
    return Auth.currentAuthenticatedUser()
      .then(userData => userData)
      .catch(() => console.log('Not signed in'));
  }

  return (
    <div>
      <p>User: {user ? JSON.stringify(user.username) : 'None'} authorized in APP1</p>
      {user ? (
        <button onClick={() => Auth.signOut()}>Sign Out</button>
      ) : (
        <button onClick={() => Auth.federatedSignIn()}>Federated Sign In</button>
      )}
    </div>
  );
}

export default App;

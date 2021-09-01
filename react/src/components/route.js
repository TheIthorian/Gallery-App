import React from 'react';
import { Route, IndexRoute } from 'react-router';

/**
 * Import all page components here
 */
import Index from './index';
import SignIn from './components/sign-in';
import Logout from './components/Logout';

export default (
  <Route path="/">
    <IndexRoute component={Index} />
    <Route path="/sign-in" component={SignIn} />
    <Route path="/logout" component={Logout} />
  </Route>
);


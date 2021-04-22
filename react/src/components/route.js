import React from 'react';
import { Route, IndexRoute } from 'react-router';

/**
 * Import all page components here
 */
import Index from './index';
import SignIn from './components/sign-in';

/**
 * All routes go here.
 * Don't forget to import the components above after adding new route.
 */
export default (
  <Route path="/">
    <IndexRoute component={Index} />
    <Route path="/sign-in" component={SignIn} />
  </Route>
);


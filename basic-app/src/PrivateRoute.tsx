import React from 'react';
import {Route, Redirect, RouteProps, RouteComponentProps} from 'react-router-dom';

export interface WalletRouteProps extends RouteProps {
  isLogged: boolean;
  component: React.ComponentType<RouteComponentProps<any>> | React.ComponentType<any>;
}

export const PrivateRoute = ({isLogged, component, render, ...restProps}: WalletRouteProps) => (
  <Route
    {...restProps}
    render={props => !isLogged
      ? (<Redirect
        to={{
          pathname: isLogged ? '/dashboard' : '/',
          state: {from: props.location},
        }}
      />)
      : React.createElement(component, {...props})}
  />
);
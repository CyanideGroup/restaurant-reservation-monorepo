import React, {useState} from 'react';
import {Switch, Route, useHistory} from 'react-router-dom';
import {ReservationPage} from './ReservationPage';
import {MainPage} from './MainPage';
import { ApiGatewayService } from './services/ApiGatewayService';
import './styles/main.sass';
import { PrivateRoute } from './PrivateRoute';

const App = () => {
  const [apiGatewayService] = useState(new ApiGatewayService('http://localhost:5000'));
  const history = useHistory();
  const [isLogged, setIsLogged] = useState(false);
  
  return <Switch>
      <Route path='/' exact component={() => <MainPage apiGatewayService={apiGatewayService} setIsLogged={setIsLogged}/>}/>
      <Route path='/reservation' exact>
        <ReservationPage setAppContent={() => history.push('/reserved')} apiGatewayService={apiGatewayService}/>
      </Route>
      <Route exact path='/reserved' component={() => <div>Brawo! Rezerwacja przebiegla pomyślnie!</div>}/>
      <PrivateRoute
        path='/priv'
        isLogged={isLogged}
        exact
        component={() => <div>Priv hihi</div>}
      />
    </Switch>
};

export default App;

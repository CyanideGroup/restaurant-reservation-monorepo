import React, {useState} from 'react';
import {Switch, Route, useHistory} from 'react-router-dom';
import {ReservationPage} from './ReservationPage';
import {MainPage} from './MainPage';
import { ApiGatewayService } from './services/ApiGatewayService';
import './styles/main.sass';
import { PrivateRoute } from './PrivateRoute';
import { Restaurants } from './Restaurants';


const hours = {
  ['2020-05-07']: {
    ['18:00']: true,
    ['19:00']: false, 
    ['19:30']: true, 
    ['20:00']: false,
  },
  ['2020-05-08']: {
    ['18:00']: true,
    ['18:30']: true,
    ['19:00']: false, 
    ['19:30']: true, 
    ['20:00']: false,
  },
  ['2020-05-09']: {
    ['18:00']: true,
    ['18:30']: true,
    ['19:00']: true,
    ['19:30']: false,
    ['20:00']: true,
  },
  ['2020-06-22']: {
    ['22:30']: true,
    ['23:00']: false,
  }
}


const App = () => {
  const [apiGatewayService] = useState(new ApiGatewayService('https://127.0.0.1:5000'));
  const history = useHistory();
  const [isLogged, setIsLogged] = useState(false);
  
  return <Switch>
      <Route path='/' exact component={() => <MainPage apiGatewayService={apiGatewayService} setIsLogged={setIsLogged}/>}/>
      <Route path='/reservation' exact>
        <ReservationPage
          setAppContent={() => history.push('/reserved')}
          apiGatewayService={apiGatewayService}
          hours={hours}
          initialNumberOfGuests={'2'}
          restaurantName={'Restauracja'}/>
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

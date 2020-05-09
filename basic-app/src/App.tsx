import React, {useState} from 'react';
import {ReservationPage} from './ReservationPage';
import { ApiGatewayService } from './services/ApiGatewayService';
import './styles/main.sass';

const App = () => {
  const [apiGatewayService] = useState(new ApiGatewayService('http://localhost:5000'));
  return <ReservationPage apiGatewayService={apiGatewayService}/>;
};

export default App;

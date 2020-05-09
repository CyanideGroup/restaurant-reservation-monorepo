import React, {useState} from 'react';
import {ReservationPage} from './ReservationPage';
import { ApiGatewayService } from './services/ApiGatewayService';

const App = () => {
  const [apiGatewayService] = useState(new ApiGatewayService('http://localhost:5000'));
  return (
  <div>
    <ReservationPage apiGatewayService={apiGatewayService}/>
  </div>
)};

export default App;

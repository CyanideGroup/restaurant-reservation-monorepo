import React, {useState} from 'react';
import {ReservationPage} from './ReservationPage';
import { ApiGatewayService } from './services/ApiGatewayService';

const App = () => {
  const [apiGatewayService] = useState(new ApiGatewayService('https://e4fa99cd-b170-445e-a214-791fb890585c.mock.pstmn.io'));
  return (
  <div>
    <ReservationPage apiGatewayService={apiGatewayService}/>
  </div>
)};

export default App;
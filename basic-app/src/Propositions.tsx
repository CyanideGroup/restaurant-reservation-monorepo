import React from 'react';
import { ApiGatewayService } from './services/ApiGatewayService';
import { Restaurant } from './Restaurants';
import { useAsync } from './utils/useAsync';

interface PropositionsProps {
  apiGatewayService: ApiGatewayService;
  onReserve: (arg: any) => void;
}

export const Propositions = ({apiGatewayService, onReserve}: PropositionsProps) => {
  return <div className='propositions'>
    <div className='propositions-title'>
      Polecamy
    </div>
  <Proposition id='1' apiGatewayService={apiGatewayService} onReserve={onReserve}/>
  <Proposition id='0' apiGatewayService={apiGatewayService} onReserve={onReserve}/>
  </div>
};
interface PropositionProps extends PropositionsProps {
  id: string;
}
export const Proposition = ({id, apiGatewayService, onReserve}: PropositionProps) => {
  const [restaurant] = useAsync(async () => apiGatewayService.getRestaurant(id), []);
  console.log(restaurant);
  return <div className='proposition'>
  {restaurant && <Restaurant onReserve={onReserve} key={id} restaurant={restaurant}/>}
  </div>
};
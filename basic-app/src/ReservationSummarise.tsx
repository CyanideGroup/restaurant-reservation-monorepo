import React, { useState } from 'react';
import { formatDate } from './utils/formatDate';
const clockImg = require('./styles/assets/clock.svg');
const calendarImg = require('./styles/assets/calendar.svg');
const userImg = require('./styles/assets/user.svg');
import {InputChecked} from './MainPage';
import { ApiGatewayService } from './services/ApiGatewayService';
import { useHistory } from 'react-router-dom';

interface ReservationSummariseProps {
  reservation: {
    restaurantName: string;
    date: Date;
    time: string;
    guestNumber: string;
  };
  apiGatewayService: ApiGatewayService;
}

const agreement = 'Zgadzam się na...';

export const ReservationSummarise = ({reservation, apiGatewayService}: ReservationSummariseProps) => {
  const history = useHistory();
  const [email, setEmail] = useState('');
  const [agreed, setAgreed] = useState(false);

  return <div className='reservation-summarise'>
    <div className='reservation-summarise-restaurant-name'>
      {reservation.restaurantName.toUpperCase()}
    </div>
    <ReservationSummariseDetails reservation={reservation}/>
  <div className='reservation-summarise-email-input'>
    <div className='email-input-wrapper'>
      <input type='text' className='basic-input search-input email-input' placeholder='imie@gmail.com' onChange={(event) => setEmail(event.target.value)}/>
    </div>
  </div>
  <InputChecked name={agreement} changeFilter={() => setAgreed(!agreed)}/>
  {/* <InputChecked name={agreement} changeFilter={() => setAgreed(!agreed)}/> */}

  <div className='reservation-summarise-button-wrapper'>
    <button 
      disabled={!agreed || !email} 
      className='basic-button coloured-button reservation-summarise-button' 
      onClick={async () => {
        await apiGatewayService.reserve({...reservation, restaurantId: '1', email});
        history.push('/reserved', {reservation: {...reservation, email}});
      }}>
      Rezerwuj
    </button>
  </div>
  </div>;
}

export const ReservationSummariseDetails = ({reservation}: any) => {
  return <div className='reservation-summarise-date-wrapper'>
  <div className='reservation-summarise-time-wrapper'>
    <img className='reservation-summarise-date-img' src={clockImg.default} /> 
    <div className='reservation-summarise-time'>
      {reservation.time}
    </div>
  </div>
  <div className='reservation-summarise-date-date-wrapper'>
    <img className='reservation-summarise-date-img' src={calendarImg.default} /> 
    <div className='reservation-summarise-time'>
      {formatDate(reservation.date)}
    </div>
  </div>
  <div className='reservation-summarise-user-wrapper'>
    <img className='reservation-summarise-date-img' src={userImg.default} /> 
    <div className='reservation-summarise-time'>
      {reservation.guestNumber} gości
    </div>
  </div>
</div>
}
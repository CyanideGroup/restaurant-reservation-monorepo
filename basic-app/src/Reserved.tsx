import React from 'react';
import { formatDateDMY } from './utils/formatDate';
import { ReservationSummariseDetails } from './ReservationSummarise';

interface ReservedProps {
  reservation: {
    restaurantName: string;
    date: Date;
    time: string;
    guestNumber: string;
    email: string;
  }
}

export const Reserved = ({reservation: {restaurantName, date, time, guestNumber, email}}: ReservedProps) => {
  return <div className='reserved'>
    <div className='reserved-wrapper'>
      <div className='reserved-title'>
        Brawo {email}!
      </div>
      <div className='reserved-subtitle'>
        Rezerwacja 
        <ReservationSummariseDetails reservation={{time, date, guestNumber}}/> 
        w {restaurantName.toUpperCase()}. Udanej wizyty!
      </div>
    </div>
  </div>
};
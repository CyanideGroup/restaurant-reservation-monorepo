import React, {useState} from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import {ApiGatewayService} from './services/ApiGatewayService';


const formatDate = (date: Date) => {
  let month = '' + (date.getMonth() + 1);
  let day = '' + date.getDate();
  let year = date.getFullYear();

  if (month.length < 2) 
    month = '0' + month;
  if (day.length < 2) 
    day = '0' + day;

  return [year, month, day].join('-');
}

const getGuestsArray = (number: number) => {
  let array = [];
  for(let i = 0; i < number; i++){
    array.push(i+1);
  }
  return array;
}

export const ReservationPage = ({apiGatewayService}: {apiGatewayService: ApiGatewayService}) => {
  const [date, setDate] = useState(new Date());
  const [hour, setHour] = useState('');
  const maxGuestsNumber = 9;
  const numberGuestsArray = getGuestsArray(maxGuestsNumber);

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
    }
  }

  return <div>
    <div>Choose number of guests</div>
    <div>
      <ul>
        {numberGuestsArray.map((index) => 
          <li key={index}>
            {index}
          </li>
        )}
      </ul>
    </div>
    <div>Choose date</div>
    <Calendar 
      value={date}
      onChange={setDate}
    />
    <ul>
      {hours[formatDate(date)] ? 
        Object.keys(hours[formatDate(date)]).map((hour) => 
        hour ?
        <li key={hour}>
          <button disabled={hours[formatDate(date)] ? hours[formatDate(date)][hour] : false} onClick={() => setHour(hour.toString())}>
            {hour}
          </button>
        </li>
        : 
        <div>
          Nie ma wolnych terminow
        </div>
      ) :
      <div>Nie ma wolnych terminow</div>}
    </ul>

    Reservation for {formatDate(date)} {hour}
    <button onClick={async () => console.log(await apiGatewayService.reserve({date, time: hour, restaurantId: '1'}))}>Reserve</button>
  </div>
};

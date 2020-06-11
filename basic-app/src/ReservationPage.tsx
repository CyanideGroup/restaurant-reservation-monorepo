import React, {useState} from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import {ApiGatewayService} from './services/ApiGatewayService';
import './styles/ReservationPage.css';
import { formatDate } from './utils/formatDate';



const getGuestsArray = (number: number) => {
  let array = [];
  for(let i = 0; i < number; i++){
    array.push(i+1);
  }
  return array;
}

export const ReservationPage = ({apiGatewayService, setAppContent}: {apiGatewayService: ApiGatewayService, setAppContent: (arg: string) => void}) => {
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

  return (
  <div className="bigBox">
    <div className="box">
      <div className="guests">
        <div className="text">Choose number of guests</div>
        <div className="Select">
          <select>
            {numberGuestsArray.map((index) => (
              <option key={index}>{index}</option>
            ))}
          </select>
        </div>
      </div>
    <div className="date">
      <p>Choose date</p>
      <div className="calendar">
          <Calendar value={date} onChange={setDate} />
      </div>
      <div className="hours">
        <ul className="hours__list">
          {hours[formatDate(date)] ? 
            Object.keys(hours[formatDate(date)]).map((hour) => 
            hour ?
            <li key={hour} className={`one-hour__list-element ${hour}`}>
              <button 
                disabled={hours[formatDate(date)] ? hours[formatDate(date)][hour] : false} 
                className={`one-hour__button ${hour}`}
                onClick={() => setHour(hour.toString())}
              >
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
      </div>
    </div>
    <div className="reservation">
      Reservation for {formatDate(date)} {hour}
      <div className="ButtonReserve">
        <button
          className="reservation__button"
          onClick={async () => {
            console.log(
              await apiGatewayService.reserve({
                date,
                time: hour,
                restaurantId: "1",
              })
            )
            setAppContent('reserved');
          }
          }
        >
          Reserve
        </button>
      </div>
    </div>
  </div>
</div>
)};

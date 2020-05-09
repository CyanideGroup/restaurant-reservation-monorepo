import React, {useState} from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import {ApiGatewayService} from './services/ApiGatewayService';
import "./styles/ReservationPage.css";


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

  return (
    <div className="body">
      <div className="bigBox">
        <div className="box">
          <div className="part1">
            <div className="part1Inside">
              <div className="text">Choose number of guests</div>
              <div className="Select">
                <select>
                  {numberGuestsArray.map((index) => (
                    <option key={index}>{index}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
          <div className="part2">
            <div className="part2Inside">
              <div className="text">
                <p>Choose date</p>
              </div>
              <div id="wpar1">
                <Calendar value={date} onChange={setDate} />
                <div className="Hours">
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
                </div>
              </div>
            </div>
          </div>
          <div className="Reserv">
            <div className="ReservInside">
              Reservation for {formatDate(date)} {hour}
              <div className="ButtonReserve">
                <button
                  className="ReserveBut"
                  onClick={async () =>
                    console.log(
                      await apiGatewayService.reserve({
                        date,
                        time: hour,
                        restaurantId: "1",
                      })
                    )
                  }
                >
                  Reserve
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

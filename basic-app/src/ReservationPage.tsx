import React, {useState} from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import {ApiGatewayService} from './services/ApiGatewayService';
import './styles/ReservationPage.css';
import { formatDate } from './utils/formatDate';
import Select from 'react-select';
import {getGuestsArray} from './SearchBar';

interface ReservationPageProps {
  apiGatewayService: ApiGatewayService;
  setAppContent: (...args: any[]) => void;
  hours: Record<string, Record<string, boolean>>;
  initialNumberOfGuests: string;
  restaurantName: string;
}

export const ReservationPage = ({apiGatewayService, setAppContent, hours, initialNumberOfGuests, restaurantName}: ReservationPageProps) => {
  const [date, setDate] = useState(new Date());
  const [hour, setHour] = useState('');
  const [guestNumber, setGuestNumber] = useState(initialNumberOfGuests);
  const guestArr = getGuestsArray(9);

  return (
  <div className="bigBox">
    <div className="restaurant-img-wrapper">
      <img className="restaurant-img" src='https://www.scandichotels.com/imagevault/publishedmedia/qn6infvg30381stkubky/scandic-sundsvall-city-restaurant-verket-10.jpg'/>
    </div>
    <div className="box">
      <div  className="right-box">
        <div className="restaurant-name">
          {restaurantName}
        </div>
        <div className="calendar calendar-reservation">
            <Calendar value={date} onChange={setDate} />
        </div>

      </div>
      <div className="left-box">
        <div className="guests">
          <div className="select">
            <Select 
              options={guestArr}
              value={{value: guestArr[parseInt(guestNumber) - 1].value, label: guestArr[parseInt(guestNumber) - 1].label}} 
              onChange={(arg: any) => setGuestNumber(arg.value)}/>
          </div>
        </div>
        <div className="reservation-page-button-wrapper">
          <button
            className="reservation__button basic-button coloured-button"
            disabled={!hour}
            onClick={async () => {
              console.log('reserve'
                // await apiGatewayService.reserve({
                //   date,
                //   time: hour,
                //   restaurantId: "1",
                // })
              )
              setAppContent({
                date,
                time: hour,
                restaurantId: "1",
                guestNumber,
                restaurantName,
              });
            }
            }
          >
            Rezerwuj
          </button>
        </div>

      </div>
    <div className="date">
      <div className="hours">
        <ul className="hours__list">
          {hours[formatDate(date)] ? 
            Object.keys(hours[formatDate(date)]).map((element) => 
            element ?
            <li key={element} className={`one-hour__list-element ${hour}`}>
              <button 
                disabled={hours[formatDate(date)] ? hours[formatDate(date)][element] : false} 
                className={`basic-button one-hour__button ${element === hour && 'choosen'}`}
                onClick={() => setHour(element.toString())}
              >
                {element}
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
)};

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
  restaurant: any;
}
// date && !date[hour].filter(element => element.size === guests);

export const ReservationPage = ({apiGatewayService, restaurant, setAppContent, hours, initialNumberOfGuests, restaurantName}: ReservationPageProps) => {
  const [date, setDate] = useState(new Date());
  const [hour, setHour] = useState('');
  const [guestNumber, setGuestNumber] = useState(initialNumberOfGuests);
  const [tables, setTables] = useState([]);
  const guestArr = getGuestsArray(9);
  console.log(restaurant);

  const isAvailable = (date: any, hour: any, guests: any) => {
    console.log('hour:  ',  hour)
    console.log('date: ', date[hour])
    const array = date[hour].filter(element => element.size === parseInt(guests));
    setTables(array);
    console.log(array)
    return date && (array.length === 0);
  }

  return (
    <div className="bigBox">
    <div className="restaurant-img-wrapper">
      <img className="restaurant-img" src={restaurant.url}/>
    </div>
    <div className="box">
      <div  className="right-box">
        <div className="restaurant-name">
          {restaurant.name.toUpperCase()}
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
              console.log('confirmation'
                // await apiGatewayService.reserve({
                //   date,
                //   time: hour,
                //   restaurantId: "1",
                // })
              )
              setAppContent({
                date,
                time: hour,
                restaurantId: restaurant.id,
                guestNumber,
                restaurantName: restaurant.name,
                tableId: tables[0]._id,
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
                disabled={isAvailable(hours[formatDate(date)], element, guestNumber)} 
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

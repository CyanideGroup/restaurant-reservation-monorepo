import React, { useState, useRef, useEffect, RefObject } from 'react';
import { useHistory } from 'react-router';
import { formatDateDMY } from './utils/formatDate';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
const calendarImg = require('./styles/assets/calendar.svg');
import Select from 'react-select';
import { Search } from './services/ApiGatewayService';

const getPossibleHours = () => {
  var arr = [], i, j;
  for(i=0; i<24; i++) {
    for(j=0; j<4; j++) {
      const hour = i + ":" + (j===0 ? "00" : 15*j);
      arr.push({value: hour, label: hour} );
    }
  }
  return arr;
}

const getGuestsArray = (number: number) => {
  let array = [];
  for(let i = 0; i < number; i++){
    array.push({value: i+1, label:`${i+1} ${i == 0 ? 'gość' : 'gości'}`});
  }
  return array;
}

export const MainPage = ({setIsLogged, apiGatewayService}: {apiGatewayService: any, setIsLogged: (arg: any) => void} ) => {
  const history = useHistory();
  const onSearch = async (search: Search) => {
    console.log(search);
    const result = await apiGatewayService.getRestaurants(search);
    console.log(result);
  };

  return <div>Main Page
    <SearchBar onSearch={onSearch}/>
    <button onClick={() => setIsLogged(true)}>Log in</button>
    <button onClick={() => history.push('/priv')}>Go to private</button>
    
  </div>;
};


const SearchBar = ({onSearch}: {onSearch: any}) => {
  const [date, setDate] = useState(new Date());
  const [guestNumber, setGuestNumber] = useState('1');
  const [hour, setHour] = useState(date.getHours().toString());
  const [searchValue, setSearchValue] = useState('');
  const guestArr = getGuestsArray(9);
  
  return <div className='search-bar'>
    <div className='search-bar-content'>
      <div className='search-bar-element'>
        <Select  options={getPossibleHours()} value={{value: hour, label: hour}} onChange={(arg: any) => setHour(arg.value)}/>
      </div>
      <div className='search-bar-element'>
        <Select options={guestArr} value={{value: guestArr[parseInt(guestNumber) - 1].value, label: guestArr[parseInt(guestNumber) - 1].label}} onChange={(arg: any) => setGuestNumber(arg.value)}/>
      </div>
      <div className='search-bar-element'>
        <DateInput date={date} setDate={setDate}/>
      </div>
      <div className='search-bar-element'>
        <SearchInput setSearchValue={setSearchValue}/>
      </div>
      <div className='search-bar-element'>
        <button className='search-bar-button' onClick={() => onSearch({date, time: hour, guests: guestNumber, address: searchValue})}>
          Wyszukaj
        </button>
      </div>
    </div>
  </div>
}

interface SearchInputProps {
  setSearchValue: (arg: any) => void;
}

const SearchInput = ({setSearchValue}: SearchInputProps) => {
  return <div>
    <input className='basic-input search-input' placeholder='np. Warszawa' onChange={(event) => setSearchValue(event.target.value)}/>
    </div>
}

interface DateInputProps {
  date: Date;
  setDate: (date: Date) => void;
}

export const useOutsideClick = (ref: RefObject<HTMLDivElement>, callback: () => void, deps?: any[]) => {
  const handleClick = (e: MouseEvent) => {
    if (ref.current && !ref.current.contains(e.target as HTMLInputElement)) {
      callback();
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClick);

    return () => {
      document.removeEventListener('mousedown', handleClick);
    };
  }, deps);
};

const DateInput = ({date, setDate}: DateInputProps) => {
  const [calendarVisible, setCalendarVisible] = useState(false);

  const changeDate = (date: Date) => {
    setDate(date);
    setCalendarVisible(false);
  }

  const ref = useRef(null);
  useOutsideClick(ref, () => setCalendarVisible(false));

  return <div>
    <div className='data-input-wrapper'>
      <input className='basic-input data-input-input' placeholder={formatDateDMY(date)}></input>
      <div className='data-input-button-wrapper'>
        <button className='data-input-button' onClick={() => setCalendarVisible(!calendarVisible)}/>
        <img className='data-input-button-img' src={calendarImg.default}/>
      </div>
    </div>
    <div ref={ref} className='calendar'>
      {calendarVisible && <Calendar value={date} onChange={changeDate}/>}
    </div>
  </div>
};
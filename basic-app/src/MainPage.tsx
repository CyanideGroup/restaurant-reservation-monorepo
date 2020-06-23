import React, { useState } from 'react';
import { useHistory } from 'react-router';
import 'react-calendar/dist/Calendar.css';
import { Search } from './services/ApiGatewayService';
import { Restaurants } from './Restaurants';
import {SearchBar} from './SearchBar';

const lelumPolelum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

export const MainPage = ({setIsLogged, apiGatewayService}: {apiGatewayService: any, setIsLogged: (arg: any) => void} ) => {
  const history = useHistory();
  const [priceFilters, setPriceFilters] = useState([]);
  const [cuisineFilters, setCuisineFilters] = useState([]);
  const result = {
    0: {
      _id: 0,
      closes: '23:00:00',
      address: 'kfc street',
      country: null,
      cuisine: 'amerykańska',
      name: 'kfc',
      opens: '07:00:00',
      rated: null,
      description: lelumPolelum,
      pricing: '$',
      url: 'https://www.scandichotels.com/imagevault/publishedmedia/qn6infvg30381stkubky/scandic-sundsvall-city-restaurant-verket-10.jpg',
    },
    1: {
      _id: 1,
      closes: '23:00:00',
      address: 'burgerking street',
      country: null,
      cuisine: 'amerykańska',
      name: 'burgerking',
      opens: '07:00:00',
      rated: null,
      description: lelumPolelum,
      pricing: '$$',
      url: 'https://www.scandichotels.com/imagevault/publishedmedia/qn6infvg30381stkubky/scandic-sundsvall-city-restaurant-verket-10.jpg',
    }
  }
  const [restaurants, setRestaurants] = useState(result);
  const onSearch = async (search: Search) => {
    console.log(search);
    // const result = await apiGatewayService.getRestaurants(search);
    setRestaurants(result);
  };

  return <div>
    <SearchBar onSearch={onSearch}/>
    <div className='content'>
      <div className='content-wrapper'>
        <Filters setFinalPriceFilters={setPriceFilters} setFinalCuisineFilters={setCuisineFilters}/>
        {restaurants && <Restaurants 
          onReserve={(args?: any[]) => history.push('/reservation', args)}
          restaurants={restaurants}
          cuisineFilters={cuisineFilters}
          priceFilters={priceFilters}
        />}
      </div>
    </div>
  </div>;
};

const Filters = ({setFinalPriceFilters, setFinalCuisineFilters}: {setFinalCuisineFilters: (args: any[]) => void, setFinalPriceFilters: (args: any[]) => void}) => {
  const [cuisineFilters, setCuisinneFilters] = useState([]);
  const [priceFilters, setPriceFilters] = useState([]);

  const setFinalFilters = () => {
    setFinalCuisineFilters(cuisineFilters);
    setFinalPriceFilters(priceFilters);
  }

  const changePriceFilter = (filter: string) => {
    if(priceFilters.includes(filter)) {
      setPriceFilters(priceFilters.filter(element => element != filter));
    } else {
      setPriceFilters([...priceFilters, filter]);
    }
  }

  const changeCuisineFilter = (filter: string) => {
    if(cuisineFilters.includes(filter)) {
      setCuisinneFilters(cuisineFilters.filter(element => element != filter));
    } else {
      setCuisinneFilters([...cuisineFilters, filter]);
    }
  }

  const cuisines = ['amerykańska', 'włoska'];

  return <div className='filters-wrapper'>
   <Prices filters={priceFilters} changeFilter={changePriceFilter}/>
   {cuisines.map(cuisine => 
    <InputChecked name={cuisine} changeFilter={changeCuisineFilter} />)}
    <div className='filters-button-wrapper'>
      <button className='filters-button basic-button coloured-button' onClick={setFinalFilters}>Filtruj</button>
    </div>
  </div>
}

const InputChecked = ({name, changeFilter}: {changeFilter: (arg: any) => void, name: string}) => {
  return <label className="container">{name}
    <input type="checkbox" onChange={() => changeFilter(name)}/>
    <span className="checkmark"></span>
  </label>;
}

const Prices = ({filters, changeFilter}: {filters: any[], changeFilter: (arg: any) => void}) => {
  return <div className='filters-prices'>
  <PriceButton 
      price='$' 
      onClick={changeFilter}
      active={filters.includes('$')}
    />
    <PriceButton 
      price='$$' 
      onClick={changeFilter}
      active={filters.includes('$$')}
    />
    <PriceButton 
      price='$$$' 
      onClick={changeFilter}
      active={filters.includes('$$$')}
    />
  </div>
}

const PriceButton = ({onClick, price, active}: any) => {
  return <button 
    onClick={() => onClick(price)}
    className={`basic-button filters-price-button ${active && ' choosen-price'}`}>
      {price}
  </button>
}
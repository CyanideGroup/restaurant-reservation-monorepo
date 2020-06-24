import React from 'react';

interface RestaurantsProps {
  restaurants: any;
  priceFilters: any;
  cuisineFilters: any[];
  onReserve: (args?: any[]) => void;
}



export const Restaurants = ({restaurants, priceFilters, cuisineFilters, onReserve}: RestaurantsProps) => {
  return <div className='restaurants-box'>
    {Object.keys(restaurants)
      .filter(key => priceFilters.length === 0 || priceFilters.includes(restaurants[key].pricing))
      .filter(key => cuisineFilters.length === 0 || cuisineFilters.includes(restaurants[key].cuisine))
      .map((key: any) => 
        <Restaurant
          key={key}
          restaurant={restaurants[key]}
          onReserve={onReserve}
        />)}
  </div>
}

interface RestaurantProps {
  key: string;
  restaurant: {
    url: string;
    name: string;
    pricing: string
    cuisine: string;
    description: string;
  }
  onReserve:(args?: any) => void;
}

export const Restaurant = ({restaurant, key, onReserve}: RestaurantProps) => {
  return <div key={key} className='restaurant-box'>
    <div className='restaurant-box-image-wrapper'>
      <img className='restaurant-box-image' src={restaurant.url}/>
    </div>
    <div className='restaurant-box-info-wrapper'>
      <div className='restaurant-box-name'>{restaurant.name.toUpperCase()}</div>
      <div className='restaurant-box-subtitle'>
        <div className='restaurant-box-subtitle-element'>{restaurant.pricing}</div>
        <div className='restaurant-box-subtitle-element'>{restaurant.cuisine}</div>
      </div>
      <div className='restaurant-box-description'>{restaurant.description}</div>
      <div className='restaurant-box-buttons-wrapper'>
        <button className='basic-button restaurant-box-button more'>Dowiedz się więcej</button>
        <button onClick={() => onReserve(restaurant)} className='basic-button coloured-button restaurant-box-button reserve'>Rezerwuj</button>
      </div>
    </div>
  </div>
}



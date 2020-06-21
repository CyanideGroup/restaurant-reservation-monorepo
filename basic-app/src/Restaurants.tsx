import React from 'react';

interface RestaurantsProps {
  restaurants: any;
  priceFilters: any;
  cuisineFilters: any[];
}

export const Restaurants = ({restaurants, priceFilters, cuisineFilters}: RestaurantsProps) => {
  return <div className='restaurants-box'>
    {Object.keys(restaurants)
      .filter(key => priceFilters.length === 0 || priceFilters.includes(restaurants[key].pricing))
      .filter(key => cuisineFilters.length === 0 || cuisineFilters.includes(restaurants[key].cuisine))
      .map((key: any) => 
        <div key={key} className='restaurant-box'>
          <div className='restaurant-box-image-wrapper'>
            <img className='restaurant-box-image' src={restaurants[key].url}/>
          </div>
          <div className='restaurant-box-info-wrapper'>
            <div className='restaurant-box-name'>{restaurants[key].name.toUpperCase()}</div>
            <div className='restaurant-box-subtitle'>
              <div className='restaurant-box-subtitle-element'>{restaurants[key].pricing}</div>
              <div className='restaurant-box-subtitle-element'>{restaurants[key].cuisine}</div>
            </div>
            <div className='restaurant-box-description'>{restaurants[key].description}</div>
            <div className='restaurant-box-buttons-wrapper'>
              <button className='basic-button restaurant-box-button more'>Dowiedz się więcej</button>
              <button className='basic-button coloured-button restaurant-box-button reserve'>Rezerwuj</button>
            </div>
          </div>
        </div>)}
  </div>
}



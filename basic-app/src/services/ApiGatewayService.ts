export const COMMON_HEADERS = {
  Accept: 'application/json',
  //'Content-Type': 'application/json',
  'Content-Type': 'application/json; charset=utf-8'

};

const fetch = window.fetch ? window.fetch.bind(window) : () => {};

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

export const http = (baseUrl: string) =>
  (method: HttpMethod, url: string, body?: any, headers?: Record<string, string>) =>
    fetch(`${baseUrl}${url}`, {
      method,
      headers: headers || COMMON_HEADERS,
      body: body !== undefined
        ? JSON.stringify(body)
        : undefined,
    }).then(handleApiResponse);

export type HttpFunction = ReturnType<ReturnType<typeof http>>;

export async function handleApiResponse(res: Response) {
  return getJsonOrText(res).then((value) => {
    if (res.ok) {
      return value;
    } else {
      throw value;
    }
  });
}

async function getJsonOrText(res: Response) {
  return res.text().then((text) => {
    try {
      return JSON.parse(text);
    } catch (e) {
      return text;
    }
  });
}

type Reservation = {
  date: Date;
  time: string;
  restaurantId: string;
  email: string;
}

export type Search = {
  date: Date;
  time: string;
  guests: number;
  name?: string;
  address?: string;
}

const parseDate = (date: Date) => `${date.getFullYear()}.${date.getMonth()}.${date.getDay()}`;

const parseSearch = ({date, time, guests, name, address}: Search) => {
  let query = `time=${time}:00&guests=${guests}&date=2020.06.24`;
  if (name)
    query += `&name=${name}`;
  if (address)
    query += `&address=${address}`;
  return query;
}

const lelumPolelum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur.'

export class ApiGatewayService {
  private http: HttpFunction;
  constructor(apiGatewayUrl: string){
    this.http = http(apiGatewayUrl);
  }

  getDate(restaurant_id: any) {
    // return hours;    
    console.log('restaurant_id:', restaurant_id)
    return this.http('GET', `/reservation?restaurant_id=${restaurant_id}`);
  }

  reserve(reservation: Reservation) {
    
    console.log('reservation: ', reservation)
    return this.http('POST', '/reservation', {...reservation, date: "2020.06.24"});
    return this.http('POST', '/reservation', reservation);
  }

  async searchRestaurants(search: Search) {
    const searchQuery = parseSearch(search);
    // return restaurants
    const restaurants = await this.http('GET', `/search?${searchQuery}`);
    const keys = Object.keys(restaurants);
    keys.forEach(key => (restaurants[key] = {...restaurants[key], pricing: getPricing(restaurants[key].price), url: restaurants[key].img1}))
    console.log("restaruatns: " , restaurants);
    return restaurants;
  }

  async getRestaurant(id: string) {
    // return restaurants[id];
      const restaurant = await this.http('GET', `/restaurant/${id}`);
      return {...restaurant, url: restaurant.img1, pricing: getPricing(restaurant.price)}
    }
};

const restaurants = {
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
  },
  2: {
    description: 'Pierogi, kasza, kluski, gołąbki, kotlet schabowy, kotlet mielony, bigos, galareta mięsna, golonka, żurek, kapuśniak… Wszystko w przystępnych cenach!',
    closes: '23:00:00',
    address: 'Francuska 11',
    country: null,
    cuisine: 'polska',
    name: 'Dom Polski',
    opens: '08:30:00',
    rated: null,
    pricing: '$$$',
    url: 'https://images.pexels.com/photos/941861/pexels-photo-941861.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
  },
  3: {
    description: 'Prawdziwy barszcz ukraiński z kwaśną śmietaną i pączkami czosnku, placki ziemniaczane, ziemniaki, pierogi lub naleśniki. Wybierz, co chcesz.',
    closes: '23:00:00',
    address: 'Jurija Gagarina 26',
    country: null,
    cuisine: 'ukraińska',
    name: 'Prydana',
    opens: '08:30:00',
    rated: null,
    pricing: '$',
    url: 'https://images.pexels.com/photos/2067576/pexels-photo-2067576.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
  },
  4: {
    description: 'Restauracja tradycyjnej kuchni włoskiej ze starożytną historią. Otwarta w 1888 roku.',
    closes: '23:00:00',
    address: 'Jurija Gagarina 26',
    country: null,
    cuisine: 'włoska',
    name: 'La Kimontaretto',
    opens: '08:30:00',
    rated: null,
    pricing: '$$$',
    url: 'https://images.pexels.com/photos/1581384/pexels-photo-1581384.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940',
  }


};

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
  },
  ['2020-06-22']: {
    ['22:30']: true,
    ['23:00']: false,
  },
  ['2020-06-24']: {
    ['11:00']: true,
    ['11:30']: false,
    ['14:30']: false,
    ['15:00']: false,
    ['15:30']: false,
    ['16:00']: false,
    ['18:00']: false,
    ['18:30']: true,
    ['19:00']: true,
    ['19:30']: false,
    ['20:00']: true,
    ['20:30']: false,
    ['21:30']: false,
    ['22:00']: true,
    ['22:30']: false,
  }
}
const getPricing = (price: number) => {
  let pricing = '';
  for(let i = 0; i < price; i++) {
    pricing +='$';
  }
  return pricing;
}
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
  let query = `time=${time}:00&guests=${guests}&date=${parseDate(date)}`;
  if (name)
    query += `&name=${name}`;
  if (address)
    query += `&address=${address}`;
  return query;
}

const lelumPolelum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

export class ApiGatewayService {
  private http: HttpFunction;
  constructor(apiGatewayUrl: string){
    this.http = http(apiGatewayUrl);
  }

  getDate(restaurant_id: any) {
    return hours;    
    // return this.http('GET', `/reservation?restaurant_id=${restaurant_id}`);
  }

  reserve(reservation: Reservation) {
    // return this.http('POST', '/reservation', reservation);
  }

  searchRestaurants(search: Search) {
    const searchQuery = parseSearch(search);
    return restaurants
    // return this.http('GET', `/search?${searchQuery}`);
  }

  async getRestaurant(id: string) {
  return restaurants[id];
    // return this.http('GET', `/restaurant/${id}`);
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
  ['2020-06-23']: {
    ['18:00']: true,
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
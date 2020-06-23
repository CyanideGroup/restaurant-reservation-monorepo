export const COMMON_HEADERS = {
  Accept: 'application/json',
  'Content-Type': 'application/json',
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

export class ApiGatewayService {
  private http: HttpFunction;
  constructor(apiGatewayUrl: string){
    this.http = http(apiGatewayUrl);
  }

  reserve(reservation: Reservation) {
    return this.http('POST', '/reservation', reservation);
  }

  getRestaurants(search: Search) {
    const searchQuery = parseSearch(search);
    return this.http('GET', `/search?${searchQuery}`);
  }
};

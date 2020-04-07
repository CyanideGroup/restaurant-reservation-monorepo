import {Server} from 'http';
import express, {Application} from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import {basicRouter} from './basicRouter';

export class BasicServer {
  protected server: Server = {} as Server;
  private app: Application = {} as Application;

  constructor(private port: string) {}

  start() {
    this.app = express();
    this.app.set('trust proxy', true);

    this.app.use(cors({
      origin: '*',
      credentials: true,
    }));
    this.app.use(bodyParser.json());
    this.app.use('/', basicRouter());
    this.server = this.app.listen(this.port);
  }
}

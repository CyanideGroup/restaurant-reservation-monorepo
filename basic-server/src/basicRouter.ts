import {Router, Request, Response} from 'express';
import {asyncMiddleware} from './asyncMiddleware';

export const basicRouter = () => {
  const router = Router();
  
  router.get('/',
    asyncMiddleware(async (req: Request, res: Response) =>
      res.status(200)
        .type('json')
        .send({ok: 'ok'})));

  return router;
}
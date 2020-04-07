import {BasicServer} from '../src/server';
import chai, {expect} from 'chai';
import chaiHttp from 'chai-http';

chai.use(chaiHttp);


describe('BasicServer', () => {
  const port = '8888';
  const server = new BasicServer(port);

  before(() => {
    server.start();
  });

  it('returns 200 code', async () => {
    const result = await chai.request(`http://localhost:${port}`)
      .get('/');
    expect(result.status).to.deep.eq(200);
    expect(result.body.ok).to.eq('ok');
  });

  it('returns 404 code if invalid endpoint', async () => {
    const result = await chai.request(`http://localhost:${port}`)
      .get('/not-found');
    expect(result.status).to.deep.eq(404);
  });
});

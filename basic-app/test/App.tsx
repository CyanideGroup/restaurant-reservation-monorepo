import {expect} from 'chai';
import React from 'react';
import Enzyme, {mount} from 'enzyme';
import {MemoryRouter} from 'react-router';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import App from '../src/App';

Enzyme.configure({ adapter: new Adapter() });

describe('App', () => {
  it('shows Choose number of guests', () => {
    const appWrapper = mount(<MemoryRouter><App/></MemoryRouter>);
    expect(appWrapper.text().includes('Wyszukaj')).to.be.true;
  })
});

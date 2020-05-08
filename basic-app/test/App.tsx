import {expect} from 'chai';
import React from 'react';
import Enzyme, {mount} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import 'jsdom-global/register';
import App from '../src/App';

Enzyme.configure({ adapter: new Adapter() });

describe('App', () => {
  it('shows Choose number of guests', () => {
    const appWrapper = mount(<App/>);
    expect(appWrapper.text().includes('Choose number of guests')).to.be.true;
  })
});

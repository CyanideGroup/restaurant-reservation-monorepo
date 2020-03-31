import {expect} from 'chai';
import {add} from '../src/index';

describe('adds two numbers', () => {
  it('returns 4', () => {
    expect(add(2,2)).to.eq(4);
  });
});

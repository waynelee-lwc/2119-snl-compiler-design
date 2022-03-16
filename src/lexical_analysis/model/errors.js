import exp from 'constants'

var models = require('./models')

export const IllegalCharacterError      = new models('illegal character!')
export const InvailedId                 = new models.Error('invailed id')
export const InvaileNumber              = new models.Error('invailed number')
//...
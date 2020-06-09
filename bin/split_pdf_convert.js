#!/usr/bin/env node

const argv = require ('yargs').argv;
const split_pdf_convert = require('../index.js');


split_pdf_convert(typeof argv.in === 'string' ? argv.in :undefined, typeof argv.out === 'string' ? argv.in :undefined);
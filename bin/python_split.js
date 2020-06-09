#!/usr/bin/env node

const argv = require ('yargs').argv;
const pythonScript = require ('./src/pythonRun');

new pythonScript.pythonRes(typeof argv.in === 'string' ? argv.in :undefined, typeof argv.out === 'string' ? argv.in :undefined);
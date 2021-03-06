'use strict';
var _require = require('python-shell'),
PythonShell = _require.PythonShell;

 Object.defineProperty(exports, "__esModule", {
    value: true
});

exports.pythonRes = pythonRes;

function pythonRes(path = './src/example/example.md', pathOut= './example/'){
  let results = []
    return new Promise((resolve, reject) => {
      
      let pyshell = new PythonShell('./src/md_split.py', {mode: 'text', args: [path, pathOut]});
      
      pyshell.send(JSON.stringify(path));
      
      pyshell.on('message', function (message) {
        results.push(message);
      });
      
      pyshell.on('stderr', function (stderr) {
        console.log(stderr);
      });
      
      pyshell.end(function (err, code, signal) {
        if (err) reject(err);
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
        resolve(results);
      });
    });
  }

// promise reference in other files- example
 /*  pythonRes(path).then((res) => {
    console.log(res);
    let wPath = res[res.length-2];
  }, (err) => {
    alert(err);
  }); */



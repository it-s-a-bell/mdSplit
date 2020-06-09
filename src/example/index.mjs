import '../extension';
import pythonScript from '../pythonRun';

import shell  from 'shelljs';

//console call , path file in followed by path out folder
// console.log(process.argv);
// var  pathmd = process.argv[2];

// var pathOut = process.argv[3] || pathmd;


function split_pdf_convert(pathIn, pathOut){
  console.log('Starting spliting of .md file with python...')
  // run python run promise
  const res = new pythonScript.pythonRes(pathIn, pathOut)
  // once it is finished, run the convertion w/ returned path 
  .then((res) => {
    console.log ('Obtaining path from python...');
    console.log(res);
    let wPath = res[res.length-2];
    wPath = wPath.split('.').slice(0, -1).join('.');
    console.log ('Creating PDF..' + wPath + '.pdf');
    // use the shell version instead of the scripted version
    var version = shell.exec(`menneu ${wPath}.md  -o ${wPath}.pdf`, {silent:true}).stdout;
    console.log('Finishing..');
  });}

  Object.defineProperty(exports, "__esModule", {
    value: true
  });
  exports.split_pdf_convert = split_pdf_convert
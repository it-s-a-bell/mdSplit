import './src/extension';
import * as menneu from 'menneu/modules';
import fs   from 'fs';
import util from 'util';
import path from 'path';
import url  from 'url';
import pythonScript from './src/pythonRun';
//import shell  from 'shelljs';

//console call , path file in followed by path out folder
console.log(process.argv);
var  pathmd = process.argv[2];
var pathOut = process.argv[3] || pathmd;

//menneu , conversion of a single file 
const readFileAsync = util.promisify(fs.readFile);
const writeFileAsync = util.promisify(fs.writeFile);
 

const isWebpack = typeof __webpack_require__ === 'function';
let thisFileName = '';
let thisDirName = '';
if (isWebpack) {
    thisFileName = __filename;
    thisDirName = __dirname;
} else {
    // webpack reports the error:
    //    Support for the experimental syntax 'importMeta' isn't currently enabled
    //    -> use '@open-wc/webpack-import-meta-loader'
    // parcel reports the error:
    //    Support for the experimental syntax 'importMeta' isn't currently enabled
    thisFileName = url.fileURLToPath(import.meta.url);
    thisDirName = path.dirname(thisFileName);
}


async function createPDF(fileWoExtension) {
 
    try {

        const pdf = (await readFileAsync(fileWoExtension +'.md')).toString('utf8');
        const buf = await menneu.render(pdf, {}, {
            rawInput: true,
            inputFormat: 'md',
            dataFormat: 'object',
            outputFormat: 'pdf',
        });
        await writeFileAsync((fileWoExtension +'.pdf'), buf);
    } catch (e) {
        console.log(e);
        
    }
};

console.log('Starting spliting of .md file with python...')
// run python run promise
const res = new pythonScript.pythonRes(pathmd, pathOut )
// once it is finished, run the convertion w/ returned path 
.then((res) => {
  console.log ('Obtaining path from python...');
  console.log(res);
  let wPath = res[res.length-2];
  wPath = wPath.split('.').slice(0, -1).join('.');
  console.log ('Creating PDF..' + wPath + '.pdf');
  // use the shell version instead of the scripted version
  //var version = shell.exec(`menneu ${wPath}.md  -o ${wPath}.pdf`, {silent:true}).stdout;
  createPDF(wPath);
  console.log('Finishing..');
});
import './extension'; 
import * as menneu from 'menneu/modules';
import fs   from 'fs';
import util from 'util';
import path from 'path';
import url  from 'url';
import pythonScript from './pythonRun';


//call in python  script before 

// Current problem asynchronous behaviour , the path obtained is  empty , because this takes longer and its unpacked afterwards 

var  pathmd = 'C:\\Users\\isabe\\Desktop\\npm_isa\\mainmd.md'; // path of the md file to be split


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


const res = new pythonScript.pythonRes(pathmd)

.then((res) => {
  console.log ('obtaining path');
  console.log(res);
  let wPath = res[res.length-2];
  wPath = wPath.split('.').slice(0, -1).join('.')
  console.log ('parsing path to convert');
  createPDF(wPath)
  console.log( 'creating PDF...')
  
}, (err) => {
  alert(err);
});
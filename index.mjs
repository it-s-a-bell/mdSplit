import './src/extension';
import * as menneu from 'menneu/modules';
import fs   from 'fs';
import util from 'util';
import path from 'path';
import url  from 'url';
import pythonScript from './src/pythonRun';


// path of the md file to be split --> Dynamic with command line 
var  pathmd = 'C:\\Users\\isabe\\Desktop\\npm_isa\\mainmd.md'; 

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
const res = new pythonScript.pythonRes(pathmd)
// once it is finished, run the convertion w/ returned path 
.then((res) => {
  console.log ('Obtaining path from python...');
  console.log(res);
  let wPath = res[res.length-2];
  wPath = wPath.split('.').slice(0, -1).join('.');
  console.log ('Creating PDF..');
  createPDF(wPath);
  console.log('Finished');
});
const fs = require('fs');
let audiomothUtils = require('audiomoth-utils');
const path = require('path');

function expander_tree(json_file, prefix, expansionType,
     maximumFileDuration, generateSilentFiles, alignToSecondTransitions){
    /* Open input file */

    try {

        fi = fs.openSync(json_file, 'r');

    } catch (e) {

        return {
            success: false,
            error: 'Could not open input file.'
        };

    }

    /* Check the output path */


    fichier = fs.readFileSync(json_file);
    obj = JSON.parse(fichier);
    nb_fichiers = obj["nombre"];
    fichiers = obj["fichiers"]
    i = 1;
    for (const [key, value] of Object.entries(fichiers)) {
        if (fs.lstatSync(value).isDirectory() === false) {

            return {
                success: false,
                error: 'Destination path is not a directory.'
            };

        }
        console.log(i + "/" + nb_fichiers + " : " + key)
        audiomothUtils.expand(key, value, prefix,
            expansionType, maximumFileDuration, generateSilentFiles, alignToSecondTransitions);
        i += 1;
    }
    fs.close(fi);        
}
let prefix = '';
let expansionType = 'EVENT';
let maximumFileDuration = 5;
let generateSilentFiles = false;
let alignToSecondTransitions = false;

//process.argv.forEach(function (val, index, array) {
console.time()
expander_tree(process.argv[2], prefix, expansionType, maximumFileDuration, generateSilentFiles,alignToSecondTransitions)
//});
console.timeEnd()

// expander_tree(json_file, prefix, expansionType, maximumFileDuration, generateSilentFiles,alignToSecondTransitions)




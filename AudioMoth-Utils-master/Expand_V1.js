const fs = require('fs');
let audiomothUtils = require('audiomoth-utils');

let prefix = '';
let expansionType = 'EVENT';
let maximumFileDuration = 5;
let generateSilentFiles = false;
let alignToSecondTransitions = false;

let json_file = "C:/fichiers.json"
process.argv.forEach(function (val, index, array) {
    audiomothUtils.expand(array[2], array[3], prefix, expansionType, maximumFileDuration, generateSilentFiles, alignToSecondTransitions);
  });
// expander_tree(json_file, prefix, expansionType, maximumFileDuration, generateSilentFiles,alignToSecondTransitions)




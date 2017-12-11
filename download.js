var args = "";

process.argv.forEach(function (val, index, array) {
  if (index != 0 && index != 1 && index != 2) {
    args = args + " " + val;
  }
});

const alltomp3 = require('alltomp3');

var dl = alltomp3.findAndDownload(args, "./", function (infos) {
    console.log(infos.file);
});

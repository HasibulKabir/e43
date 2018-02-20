var args = "";

process.argv.forEach(function (val, index, array) {
  if (index != 0 && index != 1) {
    args = args + " " + val;
  }
});

const alltomp3 = require('alltomp3');

var dl = alltomp3.findVideo(args).then(function(results) {
    console.log(results[0].url);
});

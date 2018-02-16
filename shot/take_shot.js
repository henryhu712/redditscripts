
/*
 * Usage: ./phantomjs take_shot.js 7xi8u https://muread.com/zh
 */

var system = require("system");
var args = system.args;

var page = require('webpage').create();
page.open(args[2], function(stat) {
    console.log('Status: ' + stat);
    if (stat === "success") {
      console.log('in if')
      console.log(args[2])
      console.log(args[1])
      setTimeout(function() {
        page.render('./eedd.png');
        //page.render(args[1] + '.png');
      }, 50000);
    }
    phantom.exit();
});


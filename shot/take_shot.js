
/*
 * Usage: ./phantomjs take_shot.js https://muread.com/zh
 */

var system = require("system");
var args = system.args;

var page = require('webpage').create();
page.open(args[1], function(stat) {
    console.log('Status: ' + stat);
    if (stat === "success") {
      page.render('pageshot.png');
    }
    phantom.exit();
});


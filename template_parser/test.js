
//url = "https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5"
//var https = require('https'),
//op = {
//    host: '10.1.1.23',
//    port: 1080,
//    method: 'GET',
//    path: 'https://www.google.com'
//}
//var req = https.request(op, function (res) {
//    res.on('data', function (chunk) {
//        console.log('BODY:' + chunk);
//    });
//});
//req.on('error', function (e) {
//    console.log('Error got: ' + e.message);
//});
//req.end();

var request = require('request');
//var request = require('browser-request')
var Agent = require('socks5-http-client/lib/Agent');

	request.get({
		agentClass: Agent,
		agentOptions: {
			socksHost: '10.1.1.23',
			socksPost: 1080
		},
        headers: {
            'User-Agent': 'request'
              },
		url: 'http://zh.wikipedia.org'
		//url: 'http://www.google.com'
	},
    function(error, data, body){
        console.log(error)
        console.log(body)

    });

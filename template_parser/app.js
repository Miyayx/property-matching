/*
 * 这部分代码负责爬取对应template-name的template label
 * 没有写入文件的操作，输出是通过node app.js > result_fname 这样的重定向操作实现的，注意隐藏多于的log
 * 爬取wiki数据需要sshtunnel类型的翻墙，在node_modules/wiki_infobox/index.js中修改proxy地址与端口
 * 
 */
var infobox = require('wiki-infobox');
var fs = require('fs');
var lazy = require("lazy");
var OpenCC = require('opencc');
var opencc = new OpenCC('t2s.json');

//var page = 'Template:infobox film';
var page = 'template:infobox comics character';
//var page = 'template:infobox OS';
var language = 'zh';
var fname = '/mnt/lmy_36/wikiraw/enwiki-template-name.dat'
var fo = '/mnt/lmy_36/infobox/enwiki-template-triple.dat'

//new lazy(fs.createReadStream(fname, 'utf8')).lines.forEach(function(line) {
//	get_template_labels(line.toString(), language);
//});
//

var find_zh_cn = function(str, reg){
    var r = new RegExp(reg, "g");
    if(str.match(r) !== null){
        var start = str.indexOf(reg);
        return str.substring(start+reg.length, str.indexOf(';', start));
    } else
        return str;
}

var clean_text = function(text){
    return text.replace('<includeonly>','').replace('&nbsp;',' ').replace('<br>','').replace(/^\//,'').replace('/^[;:]|[;:]$/');
}


var get_template_labels = function(page, language) {
	var res = '';
	infobox(page, language, function(err, data) {
		if (err) {
			// Oh no! Something goes wrong!
			console.log(err)
			return;
		}

		console.log(data);
		Object.keys(data).forEach(function(key) {
			var match = key.match(/^label\d+$/);
			if (match !== null) {
				var label = '';
				// 分析label
				var o = data[key];
				if (o.type == 'text') { //如果是文本
                    o.value = o.value.replace('<includeonly>', '').replace('</includeonly>','').replace('{{#if:','');
					if (o.value.indexOf('{{nowrap|') > - 1){ 
                    var s = o.value.indexOf('{{nowrap|');
                    label = o.value.substring(s+'{{nowrap'.length, o.value.indexOf('}}', s));
                    }
                    else if(o.value.match(/{{{.+}}}/) !== null){ //{{{chrtitle|主席}}} {{{magazine<includeonly>|</includeonly>}}}
                        var labels = o.value.match(/{{{.+}}}/)[0].split('|');
                        if (labels.length == 1)
                            label = labels[0];
                        else if (labels[1].length > 0)
                            label = labels[1];
                        else
                            label = labels[0];
					    label = label.replace(/}/g, '').replace(/{/g, '').trim();
                    }else if(o.value.match(/-{.+}-/)){
                        var m = o.value.match(/-{.+}-/);
                        label = o.value.substring(0, o.value.indexOf('-{')) + m[0].substring(8, m[0].length);
                        label = find_zh_cn(label, 'zh-hans:');
                        label = find_zh_cn(label, 'zh-cn:');
                    }
					else {
                    label = o.value;
                    }
				}
				else if (o.type == 'link') { //如果是link
					var t = o.text;
                    t = find_zh_cn(t, 'zh-hans:');
                    t = find_zh_cn(t, 'zh-cn:');
					var url = o.url.split('/')[o.url.split('/').length - 1];
					if (t == url) label = '[[' + t + ']]';
					else label = '[[' + t + '|' + url + ']]';
				} else { //如果是一个list
					var l = '';
					for (var i = 0; i < o.length; i++) {
						var item = o[i];
						if (item.type == 'text' && item.value == '{{nowrap|') { //如果是这样形式的，第2个是一个link
							it = o[1];
							if (it.type == 'link') {
								var zh_hans = it.text; 
                                zh_hans = find_zh_cn(zh_hans, 'zh-hans:');
                                zh_hans = find_zh_cn(zh_hans, 'zh-cn:');

								var url = it.url.split('/')[it.url.split('/').length - 1];
								label = ('[[' + zh_hans + '|' + url + ']]');

							}
							break;
						} else if (item.type == 'text') {
							label += item.value;
						} else {
							var t = item.text;
							var url = item.url.split('/')[item.url.split('/').length - 1];
							if (t == url) {
								l += ('[[' + t + ']]');
							} else l += ('[[' + t + '|' + url + ']]');
						}
					}
					label += l
				}
				//console.log(key + label);
				//分析data
				var dl = '' // 英文dump label
				var zhdl = ''; // 中文dump label
				if (label.length > 0) {

					var n = key.match(/\d+$/)[0];
					var k = 'data' + n
					var oo = data[k];
					if (oo && oo.value) { //还有date2的情况，忽律
						var m = oo.value.match(/{{{.+}}}/);
						var value = '';
						if (m !== null) {
							value = m[0]
						} else {
							value = value.replace(/}/g, '').replace(/{/g, '').trim();
						}
						var items = value.split('|');
						dl = items[0].substring(3);
						if (items.length > 1) zhdl = items[items.length - 2].substring(3);
						//console.log(k + ' ' + dl + ' ' + zhdl);
					}
				}

				if (label.length > 0 && dl.length > 0) {
                    dl = clean_text(dl);
                    zhdl = clean_text(dl);
                    label = clean_text(label);
					var str = dl + '(' + page + ')' + '\t' + label + '\t' + zhdl
                    str = opencc.convertSync(str); //繁简体转换
					res += (str + '\n');
					console.log(str);
				}

			}

		});

	});

}

get_template_labels(page, language);

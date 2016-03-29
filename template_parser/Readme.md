
###INSTALL
```shell
sudo apt-get install gcc g++
sudo apt-get install opencc
sudo npm install
```

这部分关于文件很复杂，主要因为爬取可能会中断，而程序的处理是异步的，很容易出现重复爬取。另外原始数据上（比如template列表）也容易出现冗余
经常需要
```shell
cat filename | sort | uniq
```
来清理冗余

```shell
awk -F '\t' '{print $1}' *wiki-template-triple.dat | sort|uniq  可输出第一列的template，由此可获得已爬取的结果
```


另外爬取结果可能还有特殊字符等，需要检查并清理一下

```vim
:%s/}}}\t/\t/g
%s/<br \/>/ /g
%s/<small title//g
 Template:Protoplanetary nebula  absmag_v    absmag_v     <small>(V)</small>[[绝对星等]]
}-\n
%s/<!--.*-->//g
```

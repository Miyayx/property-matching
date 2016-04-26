### Third Package
* pip install mwparserfromhell
* pip install hanziconv

### Procedure
1. 从维基百科的dump文档中抽取与Template相关的dump信息，单独放一个文件（减少其他步骤的运行时间）
Step1 Extract Template page dump 
```python
python extract_template_dump.py  /data/dump/enwiki/enwiki-20160305-pages-xxx.xml
```
input : enwiki-xxx-pages-xxx.xml (网上下载的dump文件）
output: enwiki-xxx-template-dump.xml (和原dump文件在同一个文件夹下)

2. 抽取render label
```python
python render_label_parse.py /data/dump/enwiki/enwiki-20160305-tempalte-dump.xml /data/xlore20160223/Template

```
input: 1) Step1的template-dump文件， 2) 输出文件夹路径
output: 
    输出路径下： 
    1) xxx-template-triple.dat  template label与render label的对应关系
    2) xxx-template-inherit.dat 继承关系的template列表
    3) xxx-template-inherit-dump.dat 继承关系的template的xml格式（作为之后处理继承类模板的输入）
    4) xxx-template-redirect.dat 模板重定向关系

    当前代码路径下：
    1) xxwiki-
    2) xxwiki-
    3) xxwiki-

3. 处理继承类模板
在代码里修改输入输出
```
python inherit_render_label_parse.py
```

4. 统计与覆盖率计算
在代码里修改输入输出,与操作
```
python coverage.py
```

其实不用特别关注在意是否所有模板都成功抽取了，关键是是否所有**被使用的**模板被成功抽取了，也就是xxwiki-infobox.dat中的模板尽可能被解析了就好


人工标注了几个，在zhwiki-manual-template-triple.dat中(注意备份一下）
* Template:Infobox Olympic sport
* Template:Infobox officeholder
* Template:Infobox Chinese

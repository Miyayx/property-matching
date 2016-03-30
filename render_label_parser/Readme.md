### Third Package
* pip install mwparserfromhell
* pip install hanziconv

###Usage
Step1 Extract Template page dump 
```python
python extract_template_dump.py  /data/dump/enwiki/enwiki-20160305-pages-xxx.xml
```
output: enwiki-20160305-template-dump.xml

Step2 Parse render labels
```python
python render_label_parse.py /data/dump/enwiki/enwiki-20160305-tempalte-dump.xml

```

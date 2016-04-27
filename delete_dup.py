#-*-coding:utf-8-*-

TEMPLATE_TRIPLE="zhwiki-template-triple.dat.uniq"

def check_triple(fn):
    count = 0
    for line in open(fn):
        count += 1
        if len(line.split('\t')) == 4:
            continue
        else:
            print count, line
    
def delete(fn, output):
    d = {}
    for line in open(fn):
        t, s = line.strip('\n').split('\t',1)
        if s in d:
            continue
        d[s] = t
    with open(output, 'w') as f:
        for s, t in sorted(d.items(), key=lambda x:x[1]):
            f.write(s+"-----"+t+"-----"+s+'\n')

def replace(rep_fn, tem_fn):
    d = {}
    for line in open(rep_fn):
        ns, t, os = line.strip('\n').split('-----',2)
        if not os == ns:
            print os,ns
            d[os] = ns
    print "diff:",len(d)
    with open(tem_fn+".bak", 'w') as f:
        for line in open(tem_fn):
            t, s = line.split('\t',1)
            if s in d:
                line = line.replace(s, d[s])
            f.write(line)

if __name__=="__main__":
    check_triple(TEMPLATE_TRIPLE+'.bak')
    #delete(TEMPLATE_TRIPLE, TEMPLATE_TRIPLE+'.label.uniq2')
    #replace(TEMPLATE_TRIPLE+'.label.uniq2', TEMPLATE_TRIPLE)
    
             
    

# Usage

### NEED
* Ubuntu
    ```
    libffi-dev
    libssl-dev
    apt-get install libxml2-dev libxslt1-dev
    ```

* CentOS
    ```
    yum install libffi-devel
    yum install openssl 
    yum install openssl-devel
    yum install libxslt-devel libxml2-devell

    ```

### Install scrapy
    ```
    sudo pip install virtualenv  #安装虚拟环境工具
    virtualenv ENV  #创建一个虚拟环境目录
    source ./ENV/bin/active  #激活虚拟环境
    pip install Scrapy
    pip install bs4
    ```

### Run
    ```
    scapy crawl infobox
    ```

### Setting
    
    在infobox_crawler/settings.py下进行配置，包括各百科的url前缀，存储地址等。
    
    * 配置WIKI选择当前爬取的百科
    * 配置CONTINUE确定是否断点续爬，爬取的结果会append到相应OUTPUT
    * 配置URLLIB2确定是用urllib2.Request还是scrapy自带的Request。前者慢，后者在wiki爬过大概8w以后会被封，过一段时间才能用。

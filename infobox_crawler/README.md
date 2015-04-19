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

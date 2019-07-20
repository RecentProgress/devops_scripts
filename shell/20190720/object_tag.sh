#!/bin/bash

tagDir="/data/html/"
webDir="/var/www/html/"
gitConfig="/.git/config"



EnjoyJsDe="src/config/environment.js.product"
EnjoyJs="src/config/environment.js"




nginxdir="/etc/nginx/conf.d"
nginxexam="/WebUpdate/nginx.conf"
function url_test() {
    url="'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxx'"
    header="'Content-Type: application/json'"
    msg="'{\"msgtype\": \"text\",\"text\": {\"content\":\"$1\"}}'"
    #curl $url -H $header -d $msg
    a='curl '$url' -H '$header' -d '$msg
    eval $a
}


for i in `ls $webDir`;do


  #进入原项目目录，获取tag标签
  cd $webDir$i

  for j in `git tag|sort -nr|head -5`;do
    #进入tag项目目录
    cd $tagDir$i

    #创建标签目录并切换至目录
    mkdir $j && cd $j


    #复制项目目录至当前标签目录
    cp -a $webDir$i .

    cd $i && git fetch

    if [[ $i == "EnjoyCarWeb" ]];then
      break
    fi

    git checkout $j && cp .env.produce .env
    composer install

    #获取tag并替换.
    tag=`git status|awk '/HEAD/{print $5}'`
    httptag=`echo $tag|tr '.' '_'`
    httpurl='tag-'$i'-'$httptag
    project=$tagDir$i/$tag/$i

    #配置nginx配置文件
    servername=$httpurl'.51ucar.cn'
    nginxconf=$nginxdir/$httpurl'.conf'
    cp $nginxexam $nginxconf
    sed -i -r "s@root (/[A-Za-z]+)+;@root $project/public;@g" $nginxconf
    sed -i -r "s@server_name _@server_name $servername@g" $nginxconf
    sed -i -r "s@https://x.51ucar.cn@https://$servername@" $nginxconf

    #重载nginx配置文件
    if `sudo -u ucar nginx -t`;then
      sudo -u ucar nginx -s reload
      url_test 'tag:'$tag' \n测试连接:https://'$servername
    else
      url_test '分支名:'$2' \nnginx配置失败'
      exit
    fi
  done

done
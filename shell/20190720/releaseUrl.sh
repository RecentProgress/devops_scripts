#!/usr/bin/env bash

#!/bin/bash

tagDir="/data/html/"
webDir="/var/www/html/"
redir="/var/www/release/"
gitConfig="/.git/config"
webConfigPro="src/config/environment.js.product"
webConfig="src/config/environment.js"
nginxdir="/etc/nginx/conf.d"
itNginxConf="/WebUpdate/it_nginx.conf"
webNginxConf="/WebUpdate/web_nginx.conf"
vueNginxConf="/WebUpdate/vue_nginx.conf"

#nginx url 推送
function url_test() {

    mes=$1
    url="'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxx'"
    header="'Content-Type: application/json'"
    msg="'{\"msgtype\": \"text\",\"text\": {\"content\":\"$mes\"}}'"
                #curl $url -H $header -d $msg
    a='curl '$url' -H '$header' -d '$msg
    eval $a
}

#vue项目更新
function vue_update_tag() {

    vtag=$1
    startTime=$(ls -l package-lock.json|awk '{print $6,$7,$8}')
    git checkout $vtag
    stopTime=$(ls -l package-lock.json|awk '{print $6,$7,$8}')
                #if [ "$startTime" != "$stopTime" ];then
    /usr/bin/npm install
    /usr/bin/npx vue-cli-service build
    git checkout -- package-lock.json
                            #else
                                #	npm run build
                                    #fi
}

#web项目更新
function web_update_tag() {
    wtag=$1
    git checkout $wtag
    cp $webConfigPro $webConfig
    /usr/bin/npm install
    /usr/bin/node build/build.js

}

#it组项目鞥更新
function it_update_tag() {
    itag=$1
    git checkout $itag
    cp .env.produce .env
    composer install
}


#生成项目nginx配置文件
function nginx_url_push() {

    nobj=$1
    nnconf=$2
    ndir=$3
    ref=$4

    httptag=`echo $ref|tr '/' '_'`
    httpurl='release-'$nobj'-'$httptag
    project=$redir$nobj
    servername=$httpurl'.51ucar.cn'
    nginxconf=$nginxdir/$httpurl'.conf'
    cp $nnconf $nginxconf
    sed -i -r "s@root (/[A-Za-z]+)+;@root $project/$ndir;@g" $nginxconf
    sed -i -r "s@server_name _@server_name $servername@g" $nginxconf
    sed -i -r "s@https://x.51ucar.cn@https://$servername@" $nginxconf

    if `sudo -u ucar nginx -t`;then
            sudo -u ucar nginx -s reload
            url_test 'release:'$ref' \n测试连接:https://'$servername
    else
            url_test '分支名:'$1' '$2' \nnginx配置失败'
            exit
    fi
}

function createObj() {
	cd $redir
	git clone $url && cd $obj
	git checkout $ref
}

function objclass() {
    obj=$1
    ref=$2
    url=$3
    if [[ $i == "EnjoyCarWeb" ]];then
            if [ -d $redir$obj ];then
                web_update_tag $ref
            else
                createObj
                web_update_tag $ref
                nginx_url_push $obj $webNginxConf dist $ref
            fi

    elif [[ $i == "AgentWebPc" ]];then
            if [ -d $redir$obj ];then
                vue_update_tag $ref
            else
                createObj
                vue_update_tag $ref
                nginx_url_push $obj $vueNginxConf dist $ref
            fi
    else
            if [ -d $obj ];then
                it_update_tag $ref
            else
                createObj
                it_update_tag $ref
                nginx_url_push $obj $itNginxConf public $ref
            fi
    fi
}

objclass $1 $2 $3
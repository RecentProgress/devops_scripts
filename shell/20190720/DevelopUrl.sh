#!/bin/bash
developDir="/var/www/html"
Dir="/webdata/var/www/test/"
OriConf="/WebUpdate/tadmin.conf"
NginxConf="/etc/nginx/conf.d/$3.conf"

#钉钉推送开发分支的url链接
function url_test() {
        url="'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxx'"
        header="'Content-Type: application/json'"
        msg="'{\"msgtype\": \"text\",\"text\": {\"content\":\"$1\"}}'"
        #curl $url -H $header -d $msg
        a='curl '$url' -H '$header' -d '$msg
        eval $a
}


#钉钉推送命令是否执行成功
function ERROR_NOTICE() {
		  url="https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxx"
		  header="'Content-Type: application/json'"
		  msg="'{\"msgtype\": \"text\",\"text\": {\"content\":\"$1 $2 $3\"}}'"
		  a='curl '$url' -H '$header' -d '$msg
		  eval $a

}

function IF_TRUE() {
		  if [ $? -ne 0 ];then
					    ERROR_NOTICE $1 $2 $3
		  fi
}

function main_subject() {
        if [ ! -d $Dir$3 ];then
                if [ ! -d "$developDir/$1" ];then
                        cd $developDir
                        git clone ${GitUrl}${4}/${1}.git
                fi
                cd $Dir
#                cp -r $developDir/$1 ./$3
#                cd $3
#                #切换到所需要的分支然后拉取
                git clone -b $2 $4 $3
				cd $3

				#拉去项目代码
                git checkout -b $2
                startTime=$(ls -l composer.lock|awk '{print $6,$7,$8}')
                git pull origin $2
                stopTime=$(ls -l composer.lock|awk '{print $6,$7,$8}')
                cp .env.develop .env

                # 安装依赖包
                /usr/local/bin/composer install
				IF_TRUE

				#重启项目的队列
				/usr/local/php7/bin/php artisan queue:restart
				IF_TRUE

				#复制nginx实例配置文件
                cp $OriConf $NginxConf

                #修改nginx配置文件
                sed -i -r "s@root (/[A-Za-z]+)+;@root $Dir$3/public;@g" $NginxConf
                sed -i -r "s@server_name _@server_name $3@g" $NginxConf

                # 测试nginx配置文件是否有误
                if `sudo -u ucar nginx -t`;then
                        sudo -u ucar nginx -s reload
                        url_test '分支名:'$2' \n测试连接:http://'$3
                else
                        url_test '分支名:'$2' \nnginx配置失败'
                        exit
                fi
                echo $1 " Success"

        else
                cd $Dir
                cd $3
                startTime=$(ls -l composer.lock|awk '{print $6,$7,$8}')
                git pull origin $2
                stopTime=$(ls -l composer.lock|awk '{print $6,$7,$8}')
                cp .env.develop .env
                if [ "$startTime" != "$stopTime" ];then
                        /usr/local/bin/composer install
						IF_TRUE
                fi
						/usr/local/php7/bin/php artisan queue:restart
						IF_TRUE
                echo $1 " Success"
        fi


}

main_subject $1 $2 $3 $4
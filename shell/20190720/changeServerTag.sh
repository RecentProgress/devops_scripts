#!/usr/bin/env bash

# 定义文件路径变量
updateLog="/data/scripts/shell/update.log"
tagDir="/var/www/html"
webConfigPro="src/config/environment.js.product"
webConfig="src/config/environment.js"

# 正确绿色显示
function green_colour() {
	echo -e "\033[32m ${1} \033[0m"
}

# 失败以红色显示
function red_colour() {
	echo -e "\033[31m ${1} \033[0m"
}


#php的laravel项目
function it_update_tag() {
	 cd ${tagDir}\/${1}
	 git checkout $2
	 cp .env.produce .env
	 composer install
	 last_check
#	 php artisan config:clear
#	 last_check
#    php artisan config:cache
#	 last_check
#	 php artisan view:clear
#	 last_check
#	 php artisan view:cache
#	 last_check
     # 清理opcache缓存
	 TE=`curl 127.0.0.1:47289/opcache.php`
	 if [  $TE != "bool(true)" ];then
		red_colour "清理opcache失败"
		exit 1
	 fi
	 php artisan queue:restart
	 last_check
}


# node.js项目
function web_update_tag() {
	cd ${tagDir}\/${1}
	git checkout $2
	cp $webConfigPro $webConfig
	/usr/bin/npm install
	/usr/bin/node build/build.js
	cd $tagDir
	green_colour "拷贝最新的Web项目目录"
       	rm -rf EnjoyCarWeb_Pro && cp -a EnjoyCarWeb EnjoyCarWeb_Pro
	last_check

}

# 检查是否执行失败，如果失败则退出脚本
function last_check() {
	if [ $? -eq 0 ];then
		green_colour "执行成功..."
	else
		red_colour "执行失败，请检查！"
		exit 2
	fi
}


#利用python脚本来实现切换负载（服务器在阿里云，使用的阿里云提供的api）
function change_load() {
	python3 /data/scripts/python/changeWeight.py $1
}

# 项目利用git管理，选择项目及所切换的标签
function select_arg {
	cd $tagDir && ls
	green_colour "请选择要更新的项目："
	read obj[$i]
	#echo ${obj[$i]}


	if  [ ! -n "${obj[$i]}" ] ;then
		break
	fi
	#进入项目对应目录
	cd ${obj[$i]} &> /dev/null

	#判断obj变量

	git fetch
	green_colour "最近的5个标签如下"
	git tag|sort -nr|head -5
	green_colour "请选择要切换的标签"
	read tag[$i]
	green_colour "***********************"
	#判断tag变量

}


# 更新项目，这里使用了shell的数组
function A_change_tag() {
	if [ ${obj[$i]} == "EnjoyCarWeb" ];then
		 web_update_tag ${obj[$i]} ${tag[$i]}
	else
		 it_update_tag ${obj[$i]} ${tag[$i]}
	fi
}

#选择项目及标签
green_colour "选择项目及标签: "
for i in {1..10};do
	select_arg
done

#切换负载至B
green_colour "将负载全部切换至C服务器...."
change_load C
last_check
sleep 30

#在A上切换标签
green_colour "在A上切换标签"
for i in `seq ${#tag[@]}`;do
	A_change_tag
done

#切换负载至A
green_colour "将负载全部切换至A服务器...."
change_load A
last_check
sleep 30

green_colour "在C上切换标签"

for i in `seq ${#tag[@]}`;do
	ssh -p *** root@hostip "sudo -u nginx bash /data/scripts/shell/tag_updata.sh ${obj[$i]} ${tag[$i]} && exit"
done

green_colour "切换负载至AC"
change_load AC
last_check

green_colour "上线完成.."
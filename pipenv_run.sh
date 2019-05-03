#/bin/sh

sleepForAWhile(){
    local timeNum=$1
    sleep ${timeNum} &
    wait
    echo "SleepForAWhile is end.timeNum:${timeNum}"
}

# 算法服务器 port:14000
nohup pipenv run python manage.py runserver 0.0.0.0:14000 > server.log 2>&1 &

# 等待10s，为了使算法服务器完全启动
sleepForAWhile 12 &

# celery 多线程
nohup pipenv run celery -A pai_algorithm worker -l info > celery.log 2>&1 &

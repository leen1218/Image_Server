#! /bin/sh

# restart redis database
#for pid in $(ps axu | grep redis-server | grep -v grep | cut -c 10-14); do
#    echo $pid
#    kill -9 $pid
#done

#/usr/local/bin/redis-server /usr/local/etc/redis.conf

for pid in $(ps axu | grep main.py | grep -v grep | cut -c 15-21); do
    echo $pid
    kill -9 $pid
done

python main.py

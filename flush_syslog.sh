# script to flush syslog to clear any preivously logged data

sudo truncate -s 0 /var/log/syslog
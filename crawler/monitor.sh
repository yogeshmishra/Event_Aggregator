#!/bin/bash
NOTIFYEMAIL=debjyotipaul385@gmail.com
#SMSEMAIL=<cell phone number @ sms-gateway>
SENDEREMAIL=alert@localhost
SERVER=http://localhost:8050
PAUSE=80
FAILED=0
DEBUG=1
COUNT=0
while true 
do
/usr/bin/curl -sSf $SERVER > /dev/null 2>&1
CS=$?
# For debugging purposes
if [ $DEBUG -eq 1 ]
then
    echo "STATUS = $CS"
    echo "FAILED = $FAILED"
    if [ $CS -ne 0 ]
    then
        echo "$SERVER is down"

    elif [ $CS -eq 0 ]
    then
        echo "$SERVER is up"
    fi
fi

# If the server is down and no alert is sent - alert
if [ $CS -ne 0 ] && [ $FAILED -eq 0 ]
then
    FAILED=1
    if [ $DEBUG -eq 1 ]
    then
        echo "$SERVER failed"
	echo `date`
    docker run -p 8050:8050 scrapinghub/splash 
	#java -jar target/dropwizard-sample-1.0-SNAPSHOT.jar server src/main/resources/sample.yml >> logfile.log 2>&1 &
	#python /home/ubuntu/metonym_galaxy/runserver.py &
    fi
    if [ $DEBUG = 0 ]
    then
        echo "$SERVER went down $(date)" | /usr/bin/mailx -s "$SERVER went down" -r "$SENDEREMAIL" "$SMSEMAIL" 
        echo "$SERVER went down $(date)" | /usr/bin/mailx -s "$SERVER went down" -r "$SENDEREMAIL" "$NOTIFYEMAIL" 
	echo `date`
    docker run -p 8050:8050 scrapinghub/splash 
	#java -jar target/dropwizard-sample-1.0-SNAPSHOT.jar server src/main/resources/sample.yml >> logfile.log 2>&1 &
	#python /home/ubuntu/metonym_galaxy/runserver.py &
    fi

# If the server is back up and no alert is sent - alert
elif [ $CS -eq 0 ] && [ $FAILED -eq 1 ]
then
    FAILED=0
    if [ $DEBUG -eq 1 ]
    then
        echo "$SERVER is back up"
    fi
    if [ $DEBUG = 0 ]
    then
        echo "$SERVER is back up $(date)" | /usr/bin/mailx -s "$SERVER is back up again" -r "$SENDEREMAIL" "$SMSEMAIL"
        echo "$SERVER is back up $(date)" | /usr/bin/mailx -s "$SERVER is back up again" -r "$SENDEREMAIL" "$NOTIFYEMAIL"
    fi
fi
if [ $COUNT -eq 500 ]
then
   PID=`lsof -i :8080 | grep java | head -1 | awk '{printf "%s\n", $2}'`
   kill -9 $PID
   echo `date`
   docker run -p 8050:8050 scrapinghub/splash
   #java -jar target/dropwizard-sample-1.0-SNAPSHOT.jar server src/main/resources/sample.yml >> logfile.log 2>&1 &
   echo "RESTARTING SERVER "
   COUNT=0
fi
sleep $PAUSE
COUNT=$((COUNT + 1))
done

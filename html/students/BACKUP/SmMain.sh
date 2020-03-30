#10/06/07 htc - built this .sh (shell) for Kris (PHP) to call as a partial solution to 
#               the file permission issues we were having with "www-data" as Apache2 "owner".
#  We ALSO changed the /etc/apache2/apache2.conf file to use USER: pi and GROUP: pi
#
######echo "Start SmMain.sh" > /home/pi/SmMain.out

echo "Start SmMain.sh with following runtime argument as SESSION NUMBER:" > /var/www/html/students/LastSession.out
echo $1 >> /var/www/html/students/LastSession.out

echo "Start SmMain.sh with following runtime argument as SESSION NUMBER:" > /var/www/html/students/PitchSessionFiles/LastSession.out
echo $1 >> /var/www/html/students/PitchSessionFiles/LastSession.out



# 10/26/18 htc - added following lines to "stop" any "ghost" SmMain.py processes that might be hanging on.
#SmSmainShellPreStopTextFile.txt   HAS "CleanUp" in it as reason the offending script will get to end.

cp /home/pi/SmSmainShellPreStopTextFile.txt /home/pi/NetworkShare/stop.txt

echo "cp /home/pi/SmSmainShellPreStopTextFile.txt /home/pi/NetworkShare/stop.txt"

# give it a couple seconds to end
echo "Sleep 2 seconds"
sleep 2.0

#10/29/18htc  if try "double file" copy 2nd stop.txt to here:   '/var/www/html/students/stop.txt'


echo $1
sudo python SmMain.py $1

echo /var/www/html/students/PitchSessionFiles/$1




# /var/www/html/students/MainLog.txt
LOGFILE="/var/www/html/students/MainLog.txt"
echo $LOGFILE
if [ -f $LOGFILE ]; then
#  cp /var/www/html/students/MainLog.txt
   cp /var/www/html/students/MainLog.txt /var/www/html/students/PitchSessionFiles/MainLogSess_$1
else
   echo "MainLog.txt file does not exist."
fi

#11/04/18 htc - added call to pitch uploader with current session.
cd /home/pi
sudo python PitchUploader.py $1 > /home/pi/PitchUploaderRedirectOutput.txt



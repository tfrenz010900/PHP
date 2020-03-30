#11/09/18 htc
cd /home/pi

if [ -f /home/pi/Cam1-background.png ] 
then

  if [ -f /var/www/html/students/PitchSessionFiles/Cam1CriticalFrame.jpg ] 
  then
    sudo rm /var/www/html/students/PitchSessionFiles/Cam1CriticalFrame.jpg
  fi

  sudo cp /home/pi/Cam1-background.png /var/www/html/students/PitchSessionFiles/Cam1CriticalFrame.jpg
  sudo chmod 777 /var/www/html/students/PitchSessionFiles/Cam1CriticalFrame.jpg
  sudo chown pi /var/www/html/students/PitchSessionFiles/Cam1CriticalFrame.jpg

fi 

if [ -f /home/pi/Cam2-background.png ] 
then

  if [ -f /var/www/html/students/PitchSessionFiles/Cam2CriticalFrame.jpg ] 
  then
    sudo rm /var/www/html/students/PitchSessionFiles/Cam2CriticalFrame.jpg
  fi

  sudo cp /home/pi/Cam2-background.png /var/www/html/students/PitchSessionFiles/Cam2CriticalFrame.jpg
  sudo chmod 777 /var/www/html/students/PitchSessionFiles/Cam2CriticalFrame.jpg
  sudo chown pi /var/www/html/students/PitchSessionFiles/Cam2CriticalFrame.jpg

fi 
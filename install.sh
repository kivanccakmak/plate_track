sudo apt-get update wget 
wget -O http://deb.openalpr.com/openalpr.gpg.key | sudo apt-key add -
 echo "deb http://deb.openalpr.com/master/ openalpr main" | sudo tee /etc/apt/sources.list.d/openalpr.list
 sudo apt-get update
 sudo apt-get install openalpr openalpr-daemon openalpr-utils libopenalpr-dev
 sudo apt-get install python-qt4
 python initializer.py data/garage.sqlite


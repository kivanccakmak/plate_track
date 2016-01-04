#plate-track
------------
Ultimate goal is constructing a software for autonomous garage door 
which would use alive camera to recognize entering car and ardunio to
open the door.

Currently, offline plate recording is done. 

<br>
**_sqlite3_** used to create database
<br>
**_pyqt_** used to introduce user interface
<br>
**_openalpr_** is used to recognize car plates


##Dependencies

```
wget -O - http://deb.openalpr.com/openalpr.gpg.key | sudo apt-key add -
echo "deb http://deb.openalpr.com/master/ openalpr main" | sudo tee /etc/apt/sources.list.d/openalpr.list
sudo apt-get update
sudo apt-get install openalpr openalpr-daemon openalpr-utils libopenalpr-dev
sudo apt-get install python-qt4
```

##Usage

```
python initializer.py
python ui.py
```

![Not](img/not_in_garage.png)
![Record](img/record_car.png)
![View](img/view_cars.png)
![In](img/in_garage.png)

##Beneficial

```
sudo apt-get install sqliteman
```







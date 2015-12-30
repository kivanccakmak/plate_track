#plate-track
------------
Ultimate goal is construct software for automatic garage door, 
which would use alive camera to recognize cars and ardunio to
open door.

Currently, offline plate recording is done. 

**_sqlite3_** used to create database.
**_pyqt_** used to introduce UI, which enables usage.
**_openalpr_** is used to recognize cars.


Dependencies:

```
sudo apt-get install openalpr
sudo apt-get install python-qt4
```

Beneficial:

```
sudo apt-get install sqliteman
```

Usage:

```
python ui.py
```





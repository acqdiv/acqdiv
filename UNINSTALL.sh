sudo python3 setup.py install --record files.txt
sudo xargs rm -rf < files.txt
sudo rm files.txt

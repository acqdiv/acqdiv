import os
from shutil import copyfile

os.mkdir('cha')

for folder in os.listdir('.'):
    if os.path.isdir(folder) and folder != 'cha':
        for cha_file in os.listdir(folder):
            cha_path = os.path.join(folder, cha_file)
            copyfile(cha_path, os.path.join('cha', folder + '_' + cha_file))

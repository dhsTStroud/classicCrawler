from distutils.core import setup
import py2exe

FILES = ['Classic Crawler', 'settings', 'breadboard', \
         'rooms', 'sprites', 'sprite_list']
FILES = [aFile + '.py' for aFile in FILES]

setup(console=FILES)

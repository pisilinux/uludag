# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upload.ui'
#
# Created: Pzt Ara 19 23:31:30 2005
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20051013
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *


image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x20\x00\x00\x00\x20" \
    "\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\x00\x00\x08" \
    "\x7d\x49\x44\x41\x54\x58\x85\xe5\x97\x7f\x4c\xdc" \
    "\xf5\x19\xc7\x5f\xa7\x57\xf3\xbd\x5a\xf4\xce\xa1" \
    "\x39\x32\x9a\xdc\x4d\x9a\x00\xe1\x0f\x8a\xd2\x14" \
    "\x56\xcd\x40\x5d\x14\x74\x69\x8f\xd5\xc4\x23\xce" \
    "\x08\xba\xc5\xa2\x73\x06\x5c\xd2\x00\x6e\xae\xf4" \
    "\x0f\x57\xea\xd2\x09\x2e\xce\x5e\x9d\x96\x3b\xa3" \
    "\x05\x8c\xb6\xa5\xc6\x0e\xea\xea\x7a\x2e\x6d\xf8" \
    "\x91\xb6\x40\x27\x1b\xd7\xd9\x06\xc8\xd2\x71\x67" \
    "\x4b\xee\x3e\xb6\x5f\xfb\xde\x1f\x77\xb4\xa5\xb2" \
    "\x75\xfb\x6b\x7f\xec\xf3\xcf\x93\xcf\xe7\x73\x79" \
    "\x9e\xf7\xf3\xbc\xdf\xcf\xf3\xf9\x1e\xfc\xbf\x2f" \
    "\xc7\x62\x87\x92\xae\x03\xee\x66\x77\xe7\x4a\x72" \
    "\x2b\x96\x70\x2c\x02\x2b\xaa\x60\x38\x0c\x2b\x6a" \
    "\x60\x38\x04\xfe\x00\x1c\x8b\x80\xaf\x0a\x46\xc2" \
    "\x90\x57\x03\xc7\xc3\x90\x07\x1c\x37\x90\x1f\x80" \
    "\xe3\x11\xc8\x87\xb1\x33\xfe\x2f\x0a\x5b\xf7\x7e" \
    "\xe8\xb8\xcd\xf1\xb7\x6b\x02\xd0\xd1\xfe\x15\x58" \
    "\x05\x3b\x38\x12\xfa\x36\x2b\x6b\x1d\x1c\x0f\x43" \
    "\x91\x95\x76\x5a\x54\x0b\x27\xc2\x90\x6f\xc1\x09" \
    "\x20\xbf\xe6\xf2\xfe\xdf\xdd\xc7\x0d\xb1\x93\xe3" \
    "\x29\x7f\xc2\x6c\xa3\xb5\xe3\x05\xc7\x6d\xdf\xba" \
    "\xb0\x28\x00\x7d\x3e\xea\xc5\x78\xfe\xc8\x48\xe8" \
    "\x76\x7c\x55\xf0\x69\x28\x93\x79\xe4\xb2\xf5\x05" \
    "\x60\x24\x94\x0e\x32\x92\xc9\x74\x24\x9d\x69\xf4" \
    "\xb8\xa1\x3c\x3f\x00\xc7\x7a\x01\xd8\x6b\xa7\xa8" \
    "\x76\xd6\x42\x56\x1f\xac\xdf\x04\xa7\x0e\x08\x0a" \
    "\x5e\x61\x43\xfd\xb3\x0e\x87\x63\x31\x00\xb3\xbf" \
    "\xe2\x93\xce\x9f\x90\x98\x26\x35\x97\xc0\x65\x0c" \
    "\x29\x63\x70\xd9\xa9\xcc\x1e\x52\x73\x71\x5c\x17" \
    "\x20\x66\x0c\x7e\x2c\xa2\xc6\x50\x6e\xc3\x5e\xdb" \
    "\x50\x6d\x43\xc8\x36\x04\x81\x1d\xb6\x21\xe8\xb4" \
    "\x88\xd8\x86\x00\x10\xb6\xa1\xa9\xb4\x8c\x98\x2f" \
    "\xc7\xf6\x67\x37\x97\x3a\x9e\xbd\x63\x04\xe0\xba" \
    "\x2b\x78\x77\x30\x12\x59\xc7\xf2\x4a\x30\x06\xd7" \
    "\xca\x7a\x78\xa0\x0e\xd7\x93\x5d\x60\x79\x70\xe5" \
    "\x05\xd3\xe7\x17\x5c\x60\x83\xbf\xb4\x01\xfc\x85" \
    "\x94\x3f\xde\xc1\xd0\xf2\x1c\xaa\x9d\x16\xe1\xf9" \
    "\xa0\x40\xd0\x69\x11\x2d\x58\x49\xc3\xaf\x47\x89" \
    "\xad\xdf\x40\xad\xd3\xa2\xfd\xc8\xa7\xf8\xb3\xe3" \
    "\xce\xe8\x9f\x9e\x58\xb7\x98\xf0\x96\x2a\x3c\x9a" \
    "\x4a\x6e\xab\x93\xb6\xd5\x49\x53\x93\xd2\xac\xa4" \
    "\xa1\x7e\x49\x92\x0e\x76\x4b\x9d\x87\x94\xec\xdb" \
    "\x9e\xde\x27\x93\x69\x33\x7f\xff\xf7\x29\x69\x56" \
    "\x1a\xdd\xd6\x28\x6d\xac\x53\x72\xe8\x90\x24\x69" \
    "\x70\x6b\x63\xda\xbe\xd4\xa8\xc9\x7c\xd4\x51\x64" \
    "\x49\x8f\x96\xbd\xb1\x18\x80\x6c\xbd\xd6\x68\xab" \
    "\x6f\x8f\x34\xd0\x95\x76\xfa\x7c\x85\xd4\xb9\x45" \
    "\x7a\xbe\x2a\x13\x44\xd2\xd8\xac\xd4\x1a\x94\x36" \
    "\x97\xa9\x7f\x8d\x57\x5a\xe3\x55\xf7\x9d\x6e\xe9" \
    "\xc1\x02\x0d\x6e\x0c\x4a\x63\x49\xe9\xbc\xa4\xe8" \
    "\xa4\x3a\x8a\x2c\x4d\x15\x59\xea\xba\xd7\x27\x49" \
    "\xea\x58\xed\xd5\x64\x3e\xea\x5e\x5b\xd0\x3d\x1f" \
    "\xf7\x12\x05\x9c\x8b\x67\x61\x52\x8e\xd4\x70\x04" \
    "\xb2\xcb\x21\x36\x04\x36\xa4\x8e\x47\xc0\x69\xc1" \
    "\xb9\x38\xcc\xa5\xc0\x1e\x87\x13\xc3\x4c\xfb\x02" \
    "\x54\x02\x3d\xc6\x50\x05\x84\x4e\xc7\xf0\xef\xeb" \
    "\xa5\xf3\xe1\xa5\xf0\x9b\x21\xe2\xf6\x18\x01\x0c" \
    "\x61\xdb\x50\x6b\xb9\x48\x4d\x0c\x11\x98\x4b\x10" \
    "\xb6\xa1\x6a\x2e\x75\xb3\xa4\xab\x00\x64\x79\x96" \
    "\x61\x8c\xc3\x55\x10\x80\x5d\x4d\xe0\x2f\x81\x87" \
    "\x1a\x70\xe5\x5b\xb0\xae\x01\x66\x80\x9d\x4f\x83" \
    "\xc9\x21\x1a\x8f\x93\xb3\xb3\x93\xbd\xb6\xa1\xc6" \
    "\x09\xbd\x19\xee\x7b\xed\x34\xf7\xa1\x9d\xf7\xe0" \
    "\xb9\xab\x9a\xa1\xd2\x0a\x1a\x7c\x05\xf0\x72\x37" \
    "\xae\x91\x04\x21\x93\x16\x64\xaf\x31\xee\xaf\x8d" \
    "\x00\x1d\xed\x5f\xa3\xcd\xc1\x8b\xc9\xd6\x2a\x69" \
    "\x63\x95\x92\x2f\xd5\xa5\xcb\x7e\x76\x56\x92\x34" \
    "\xdb\x1a\x4c\x73\x79\xbf\x4f\x7a\x69\x83\xf6\xac" \
    "\x76\x4b\xab\xdd\xea\x2a\xb6\x94\x2c\xb6\xb4\xbd" \
    "\xc8\xd2\x6c\xb1\xa5\x8e\x22\x34\x55\x84\x0e\x6d" \
    "\x0c\x5e\xd6\xca\x59\x69\x4b\x3e\x1a\xcd\x43\x9b" \
    "\xf2\xd0\xec\x1a\xdf\x9f\x75\x76\xf6\xfa\x85\x15" \
    "\xf0\x56\xde\x82\x6d\x1c\xae\xfc\x20\x98\x14\xae" \
    "\x65\xe3\xb0\x3f\x0c\x59\x1e\x78\xab\x1d\xcf\x70" \
    "\x94\xb1\x75\x85\x94\xd8\xc0\xbe\xde\x8c\xea\x21" \
    "\x90\x51\x7d\xc0\x49\xa6\xe5\xd2\x95\xf0\xef\xeb" \
    "\x85\x89\x21\x70\xb9\x08\x3f\x5c\x48\x0d\xd0\x0b" \
    "\x04\x80\x08\xe6\x46\xb2\x3c\x0e\x80\xeb\xe7\xe3" \
    "\xff\xbc\xec\xd6\x52\x86\xa2\x81\xbd\x07\x3e\xe0" \
    "\xd6\xb1\x93\x6c\x1d\xf8\x0b\x77\x1b\x48\x15\xaf" \
    "\x62\xa2\xfe\xfb\x6c\x9b\x39\xc3\xa9\xc4\x1c\xc3" \
    "\xc9\x39\x56\x5d\x84\x1e\x6c\xbe\x77\x31\x1d\x34" \
    "\x08\xbc\x0b\x3c\x7c\x9d\x93\x77\xcf\x1b\x02\x4e" \
    "\x08\x9f\xb7\x29\x9f\x39\x0d\xab\x2a\xc9\x7a\xe5" \
    "\x45\xc2\xe7\x6d\x00\x86\x6d\x78\x6c\xe9\xb2\x8b" \
    "\x59\xdf\xe0\xe5\x17\xdf\xd9\xff\xd5\x65\x0a\xb6" \
    "\x6e\xdf\xd0\x98\x8b\x06\x7d\x68\xde\xea\x83\x2e" \
    "\xe9\xcd\x7e\x35\xe6\xa2\xc9\x22\xb7\xba\xd7\xae" \
    "\x94\x3e\x1a\x94\x3e\xea\x4e\xab\xfa\x4e\xb7\x66" \
    "\x8b\x2d\x0d\xb6\x06\xa5\xa4\xa4\x21\x49\xa1\x6e" \
    "\xed\x59\x5b\xa0\xa9\x62\x4b\x5b\xf2\x91\x24\x75" \
    "\x3f\x5a\x71\xa9\xfc\xa3\x79\xa8\xa3\xc8\x32\x9a" \
    "\x4c\xde\x04\xe0\x9c\x07\xd0\xf3\x49\xe7\x4d\x41" \
    "\x27\x44\x6c\xb0\x32\xb6\x64\x75\x2d\xe1\x67\xcb" \
    "\xb1\x9c\xd0\x99\x48\x10\x1c\x19\xa6\xa9\xee\x0e" \
    "\x2c\x27\x04\x9f\x6a\xa4\x22\x61\xd8\x6c\x0c\xed" \
    "\x09\x43\x4f\x7d\x09\xe5\xe3\xe3\x84\x8d\x01\x60" \
    "\x1c\xa8\x01\x62\xbb\x43\xd4\x64\xe7\xd0\x66\xcf" \
    "\xd3\x04\x6e\xc3\x0d\xf1\x93\x03\x4b\x81\xb3\x97" \
    "\x34\x50\x33\x67\xdc\x11\x1b\x82\x4e\x30\x19\xcb" \
    "\xc7\x21\x6a\xef\x6d\xbe\xb4\xbf\xf2\xbe\xf0\xae" \
    "\x3a\x76\x18\x43\xd0\x09\x9d\x47\xa2\xd4\xac\x6b" \
    "\x27\x34\x67\xa8\x75\x5a\x00\x34\x3d\x52\xc6\x80" \
    "\xd7\x87\xff\xfe\x7a\x7a\x66\x62\x97\x82\x07\x81" \
    "\x84\x6d\x1c\x9e\xa2\xea\xac\x05\x22\x0c\x81\xc7" \
    "\xba\x22\x48\xc4\x06\x62\xe3\x0c\xd9\xe3\x04\xc9" \
    "\x54\x06\x32\xad\x06\x3d\xaf\x3c\x01\x99\xf3\xb2" \
    "\x33\x09\xc2\xbb\x5a\x30\x36\x74\xce\x19\xea\xbd" \
    "\x3e\xf6\x9e\xb4\x08\xd8\x06\xe6\xe2\x94\x4f\xc4" \
    "\xd2\xfe\x80\x1d\x36\x04\x6c\x98\xfe\xb8\x7d\x21" \
    "\x80\x80\x33\x78\xd3\xd5\x99\xf6\x1c\x1f\xa7\x64" \
    "\x7d\x53\x66\xb6\x83\xb5\xcc\xa2\xed\xa9\x0a\x22" \
    "\x36\xd4\x7c\xa7\x91\xf6\x1d\xdd\xb4\x1f\x16\x25" \
    "\xaf\x76\x51\x19\x8b\x61\x6c\x68\x7b\x6e\x3b\x11" \
    "\xa0\xfa\x91\x0e\x3c\xf7\x05\xc0\xe3\xa1\xf3\xcc" \
    "\x0c\x01\x2e\x57\x36\x02\xe4\xa4\x72\x16\x02\x88" \
    "\x98\xd0\xcd\x97\x34\x90\xc9\xac\xe4\x58\x14\xec" \
    "\x69\xbc\x6e\x37\x11\x1b\x5a\x9e\x19\x23\x3c\x92" \
    "\xe6\xb8\xfd\xf5\xa7\xe1\xbe\x1a\xc8\x01\xa6\xcb" \
    "\xe9\x9c\x99\x21\x08\x8c\x65\x1b\x02\x36\xb4\xbf" \
    "\x70\x0f\x38\x6b\x89\xbd\x17\x02\xfb\xaa\xca\x02" \
    "\xb1\xb7\x5b\xac\x05\x83\x68\x76\xb5\xf7\x0f\x57" \
    "\x77\x41\x63\x2e\x52\xdf\xa0\xf4\xb9\xd2\x0f\xd3" \
    "\x79\x49\x03\x93\xd2\x33\x01\x69\x73\x85\x3a\xee" \
    "\x2d\x90\x3e\x97\x36\xe5\x5b\x52\xa8\x5b\xfd\x4f" \
    "\x05\xd2\xbf\x39\x9a\x9e\x41\x9a\x1c\x55\xf2\xc1" \
    "\x2d\x5a\xd4\xef\x9d\xee\xea\x05\x73\x60\xb9\xd7" \
    "\xf9\x43\x63\xcc\xf2\xe1\x2b\x90\x5a\x4e\xe8\x7b" \
    "\xff\xb7\xac\x78\xff\x35\xcc\x37\x5d\x64\xe5\xaf" \
    "\x82\xdb\x80\xc3\x07\xe9\x19\x3c\xc1\xa9\x13\x31" \
    "\x9c\x76\x8c\xf2\xcf\x26\x18\xf8\x62\x82\xea\xc6" \
    "\x77\xc0\x0d\xdc\xb2\x84\x81\xe6\x5a\x42\xcd\xcf" \
    "\xb1\xff\xf4\xbe\x05\xfe\x86\xed\xf4\x30\x3a\xb8" \
    "\x8c\x48\xef\x94\x3d\x71\x89\x82\x86\xc7\x3b\x66" \
    "\x16\x53\x7b\x83\xd7\xcb\xf4\x43\x55\x58\xaf\x4e" \
    "\x43\x73\x2d\x9c\x04\x9e\x6c\xa4\x32\x91\xc2\x5f" \
    "\xbc\x92\xf2\x75\x6d\x84\x9d\x50\xf3\x60\x33\xe4" \
    "\x7a\xe0\xf7\xc3\x84\x02\x25\x54\x66\x57\xd2\xf6" \
    "\x40\x55\xe6\xa3\x64\x61\x77\xf5\x39\xa1\x36\x32" \
    "\x95\x5c\xa0\x81\x54\x69\xce\xee\x86\x0c\xd7\xf3" \
    "\xdd\x50\x67\x59\x0c\xad\xf0\xd3\xb7\x73\x07\xc3" \
    "\x05\xe3\xc4\x8f\x0c\x13\xdd\xd5\x04\xee\x42\xf8" \
    "\x65\x88\xda\x82\x95\xb4\xfd\xa0\x90\x96\xb7\x26" \
    "\x49\xdd\x55\x08\x6f\x0c\xd1\xb3\xab\x85\xfa\x15" \
    "\x7e\x3a\x77\xb7\x31\x76\x60\x80\xf1\xa2\x02\xae" \
    "\xee\xae\xb6\xfb\xaa\xe2\xe4\x5a\x43\x0b\x34\x20" \
    "\xc9\x35\xba\xad\xf9\xb3\xd1\x3c\x4b\xcd\xbe\x85" \
    "\x9c\x6d\x29\x76\x6b\x76\x8d\x4f\xfd\xcf\x05\x35" \
    "\x59\xec\xd5\x96\x22\x77\x9a\xe3\xbe\x6e\x69\x68" \
    "\x56\x1a\x93\xf4\xd1\x68\x9a\xdb\x6d\x5d\xea\x58" \
    "\xe3\x93\x5a\xcb\x16\xe5\x7e\x6a\xb5\x57\x8a\xee" \
    "\xf9\xc5\xfc\x73\xec\xb8\x0a\xc4\x9a\xd8\xcb\x0d" \
    "\x7d\xee\xb7\x23\x59\xa1\xb9\x04\x64\x5a\x27\x00" \
    "\x1c\xc8\xf6\xd2\x50\x50\x40\xcb\x81\x03\x04\x80" \
    "\xbe\x65\x16\x2d\x65\x95\x0c\x2c\x73\x53\x79\x7a" \
    "\x9a\xa6\x4f\x0f\x60\x65\xca\xdc\xbe\x3e\x48\xd3" \
    "\xae\x08\x16\x60\x48\x0f\x9f\x08\xd0\xec\xf3\xc1" \
    "\x4f\x5b\x0e\x7a\x1e\xaa\xbf\xdf\xe1\x70\xa4\xbe" \
    "\x06\x20\x03\xa2\x82\xfd\xa1\xd7\x49\xb8\x6f\x27" \
    "\xd2\x0a\x89\x38\x7b\x8d\xa1\xda\xdd\x40\xf8\xcc" \
    "\x56\xaa\xec\xcb\xaf\x5e\xd8\x36\xd4\x90\xfe\xe0" \
    "\x0c\x64\x86\x54\xc0\x09\x7d\x96\x45\x95\x81\x88" \
    "\x31\x04\x9c\x16\xc3\x3e\x2f\xf5\x3f\x0e\x7d\x45" \
    "\x6e\xea\x3d\x4a\xab\x7f\xe4\x70\x38\x66\xe7\xe3" \
    "\xfd\xab\x3f\x26\x37\x33\x11\xad\x21\xb7\xfc\x31" \
    "\x3e\x6c\x5f\xcd\xa9\xd8\x0d\xa9\x33\x33\xb8\xe6" \
    "\x0c\xf1\xb9\x38\x1e\x63\x88\x9d\x8b\xe3\xb7\x21" \
    "\x3a\x67\x28\xb7\x0d\x3d\x26\x3d\xfb\x43\x76\x7a" \
    "\x0e\xf4\xb9\x2d\x6a\x4b\x2b\x89\x97\x95\xfd\xc3" \
    "\xb3\xb6\xe9\x7d\x66\xc6\x7e\xc7\xf2\xc2\xa8\xc3" \
    "\xe1\xf8\x6a\xb1\x98\x8b\x2e\x49\x0e\x49\x05\x1a" \
    "\xd3\x26\x25\x35\xa9\x81\xed\x17\x35\x95\x94\xfa" \
    "\xb6\x4b\x63\x93\xd2\x9b\xcd\xd2\xc1\x43\xd2\xd6" \
    "\x3a\xe9\xdd\x6e\x69\x63\x55\xda\x86\x37\x9d\x57" \
    "\x52\x03\xfa\x6c\xf0\x31\x49\xee\xff\x38\xe0\x35" \
    "\xc0\x2c\x91\xf4\x5d\x1d\xed\x7f\x53\x49\xfd\x55" \
    "\x87\xf7\x7c\xa9\xb3\x92\xa2\xdd\xd2\x59\x5d\xd4" \
    "\xe1\xee\x2f\x94\xd4\x61\x8d\x1d\xfa\x99\xa4\xbc" \
    "\x79\x91\x5d\x6b\x2d\x4a\xc1\x35\x80\xc0\x05\x9c" \
    "\x2c\xe1\x46\xce\xe1\x21\x0b\x27\xe7\x48\x92\x45" \
    "\x1c\xf8\xd2\xe1\x70\x5c\xfc\x6f\x7d\xfe\x4f\xd7" \
    "\x3f\x01\xec\x7f\x32\xd9\xcc\x62\x29\x86\x00\x00" \
    "\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

class UploadDlg(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("UploadDlg")

        self.setIcon(self.image0)


        self.hardwareInfoLabel = QLabel(self,"hardwareInfoLabel")
        self.hardwareInfoLabel.setGeometry(QRect(171,61,428,26))
        hardwareInfoLabel_font = QFont(self.hardwareInfoLabel.font())
        self.hardwareInfoLabel.setFont(hardwareInfoLabel_font)
        self.hardwareInfoLabel.setTextFormat(QLabel.RichText)
        self.hardwareInfoLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.labelStatus = QLabel(self,"labelStatus")
        self.labelStatus.setGeometry(QRect(178,90,420,150))
        labelStatus_font = QFont(self.labelStatus.font())
        self.labelStatus.setFont(labelStatus_font)
        self.labelStatus.setTextFormat(QLabel.RichText)
        self.labelStatus.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.buttonRetry = QPushButton(self,"buttonRetry")
        self.buttonRetry.setGeometry(QRect(174,247,120,31))
        self.buttonRetry.setOn(0)

        self.hardwareInfoPixmap = QLabel(self,"hardwareInfoPixmap")
        self.hardwareInfoPixmap.setGeometry(QRect(-5,0,142,290))
        self.hardwareInfoPixmap.setScaledContents(1)

        self.languageChange()

        self.resize(QSize(619,287).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Feedback Wizard"))
        self.hardwareInfoLabel.setText(i18n("<h2>Upload</h2>"))
        self.buttonRetry.setText(i18n("Retry"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcomedlg.ui'
#
# Created: Pzt Ara 19 23:31:29 2005
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
    "\x69\x49\x44\x41\x54\x58\x85\xe5\x97\x6f\x8c\x5c" \
    "\x55\x19\xc6\x7f\xb7\xdc\xad\x77\xe8\x6e\x7b\xc7" \
    "\x0c\x64\xc6\xb4\xba\x57\x68\xd2\x3b\x74\x93\xce" \
    "\xd0\x2a\xbb\x16\xe2\x0e\xd6\xd8\x6e\x6a\xc2\x34" \
    "\x7c\xb0\x53\x20\x74\x05\x81\x05\x51\xb7\xc1\x10" \
    "\xfe\x44\x53\xd0\x08\x2d\xb5\xc2\x82\x86\xee\xa2" \
    "\xe2\x6c\x4d\x68\xb7\x29\xb0\xb3\xc4\xca\x6c\x83" \
    "\x30\x43\xdc\x32\x97\x40\xe9\x54\xb6\xe9\x5d\xed" \
    "\xa4\x33\xc1\x91\x7b\x61\xc7\xbd\x07\x7b\xe1\xf8" \
    "\x61\x66\xff\x5a\x50\x3f\xf9\xc1\xf3\xe5\xe4\xcc" \
    "\xb9\xf3\x3e\xcf\x79\xde\xe7\x3d\x7f\xe0\xff\xbd" \
    "\x29\xe7\xfb\x51\x4a\xb9\x88\xbf\x3a\x57\xf1\xea" \
    "\x60\x0c\x2d\xdc\x44\xd9\x82\xa0\x01\x67\x0a\xa0" \
    "\x47\xa1\x94\x83\x66\x13\x2a\x16\x34\x1b\x50\x2a" \
    "\x80\xde\x18\xeb\x40\x45\x40\xa8\x31\x0e\xc1\x09" \
    "\x8c\xf7\xa2\xb7\x3e\xfc\x82\x12\xbd\xec\xcf\xff" \
    "\x96\x80\x7c\xe3\xc5\x95\xd4\x18\xc0\xce\x7d\x89" \
    "\x15\x31\x85\x8a\x05\x61\xad\x1e\x34\x1c\x83\xaa" \
    "\x05\x21\x0d\xaa\xd4\x41\xa6\xc7\x9f\x34\xef\x08" \
    "\xec\x89\xa2\x67\xb8\x62\x2f\xf7\x3d\x76\xbf\x72" \
    "\xf1\xe7\xcf\x9d\x97\x80\xfc\xcb\x5b\x61\x4a\x95" \
    "\x97\x29\xe5\x2e\xa1\xd9\x80\xf1\x1c\xe8\x06\x94" \
    "\xac\xd9\xbe\xd9\xac\x2b\x10\xd2\xa0\xd4\x58\x69" \
    "\xc9\xc2\x0b\x81\x55\x11\x98\x21\x13\x51\x2e\x02" \
    "\x50\xf0\x3d\xe2\x6a\x1c\xad\xc5\x26\xf8\xe5\xad" \
    "\x20\x2a\x92\x2a\x8f\x72\xff\xae\x3b\x15\x45\x39" \
    "\x0f\x81\xc2\x2b\x7b\x28\x66\xbf\x83\x5b\xc6\xab" \
    "\xb9\x04\x84\xc0\x13\x82\x80\xef\x35\xc6\xe0\xd5" \
    "\x1c\x02\xe7\xc0\x16\x02\x03\x8d\x9c\x10\x18\x3e" \
    "\x14\xfc\x7a\x9f\xf7\x05\x31\x1a\xbd\xaa\x61\xf9" \
    "\x02\x13\x28\xf8\x90\x5a\xd7\x8e\x68\x8d\xf8\x46" \
    "\x28\xb9\x4e\xb9\x73\xdb\xeb\x00\x17\xcc\xc9\xbb" \
    "\xc2\xb1\x67\x7f\xce\x05\x41\x9d\xaa\x4d\xd3\x67" \
    "\xbe\x00\x5f\xec\xa4\xc9\xfc\x2a\x9c\xb6\x68\x5a" \
    "\x6c\x40\x75\x82\xa6\x0f\x9a\xc0\xf7\x09\x7e\xee" \
    "\x2a\x08\xb6\xb0\xa2\x3d\xc9\xf8\xdf\x4b\x7c\xb6" \
    "\x26\x18\x13\x35\xda\x54\x0d\xeb\x23\x9f\xb6\x45" \
    "\x2a\x8e\x19\x23\x75\xcb\x4f\x29\x5f\x1c\xe2\xa2" \
    "\x93\x6f\xf2\xbb\xd2\x04\x89\xcb\xc2\x8b\xc6\xde" \
    "\x18\x7d\x67\xe0\x78\xe5\xe8\x42\xe3\x5d\x28\xd3" \
    "\x07\xbc\xa9\xbd\xdb\xa5\xdc\xbb\x5d\xca\xb3\xa7" \
    "\xa5\x7c\xfb\xb4\x94\x85\x17\xa5\x94\x52\xca\x97" \
    "\x0e\x48\xd9\xb7\x4f\x4e\x65\xf6\x49\xf9\xbe\x94" \
    "\x72\x6a\x4a\xca\x29\x29\xa7\xa6\xe7\xdf\x39\x2b" \
    "\xe5\xdb\xa7\xe5\x5b\x7b\x7b\xe5\xd4\xdd\xdb\xe5" \
    "\x54\xe1\x15\x29\xff\x21\xe5\x6b\xbb\x7b\xa5\x7c" \
    "\x77\x4a\xbe\xf6\x93\x5e\xf9\xfc\x2a\xe4\x63\xab" \
    "\x35\xf9\xee\x75\xed\x4f\x4d\xe3\xaa\x73\x38\x5c" \
    "\x48\x2d\xdf\x14\xd0\x4d\x58\x11\x01\x35\x0c\x4f" \
    "\x76\xd5\x5d\xbe\x7f\x37\x3c\x38\x0c\xab\x20\x70" \
    "\x32\x07\x0f\xa7\xa0\x66\x93\x1d\xb3\x31\x80\x82" \
    "\x10\x74\x84\x23\x94\xdb\x62\xc4\x37\xf6\xc2\x15" \
    "\x71\x78\x61\x98\xbe\xeb\x03\x98\x40\x7a\xe4\x20" \
    "\xa9\x8c\x4d\xdf\xa1\x34\xad\x6e\x85\xec\xa4\xdb" \
    "\x32\x0d\xba\x68\x06\x7e\xd2\x69\x41\x78\x8a\x57" \
    "\xb2\x00\x1d\x6a\x45\xf0\xc1\xab\x58\xa0\x6a\x20" \
    "\x1c\x98\x28\xd4\xcb\xec\xa4\x45\x79\x6d\xb2\x9e" \
    "\x5b\x21\x30\x80\x4c\xc9\x46\x8c\x0c\xd1\x77\xdb" \
    "\xe5\xf0\x44\x1a\x47\x07\x13\x41\xc1\x17\xc4\xb4" \
    "\x00\xde\x44\x01\xb3\xe6\x62\xf9\x60\xd4\xbc\x65" \
    "\x52\xca\x05\x04\xb4\x60\x33\x42\x28\x81\x90\x09" \
    "\xa3\x03\xb0\x3c\x0e\x9b\x7b\x08\x84\x34\xb8\xa6" \
    "\x07\x8e\x17\x61\xa4\x0f\x4a\x0e\x39\xc7\x41\x7b" \
    "\xba\x8f\x82\x2f\x30\x55\x28\x36\x0c\x57\xf4\x21" \
    "\xa6\x6a\xf4\x3f\x7d\x3b\xc1\xb5\x5d\x78\xeb\x3a" \
    "\x49\xb4\x9a\x44\x1f\x39\x00\x47\xf2\xe4\x44\xdd" \
    "\x90\x45\x21\xf4\xe9\x02\x98\x4d\xc1\xc9\xec\x32" \
    "\x7c\x81\x57\xca\x13\xf0\xc1\xdb\xd3\x4d\xe0\xae" \
    "\x7e\x58\x9b\x80\x96\x20\xce\xfd\x29\x82\x77\xec" \
    "\xa3\x70\x7d\x94\x8e\x0d\x49\x86\x0f\x0d\x12\x85" \
    "\x99\xa0\x96\xa8\x93\xb1\x7c\x81\xe9\x0b\x72\x3b" \
    "\x53\x74\x0d\x64\xc1\xf3\xa0\xe2\xd2\xf7\xe8\xed" \
    "\x75\x70\x20\x81\xb6\x94\x49\x67\x11\xf0\xe1\xac" \
    "\x02\x6a\xf8\xd3\xf8\x42\x09\x84\x62\x20\x3c\x02" \
    "\xa2\x08\x47\xd2\xd0\x12\x84\x5f\xef\x22\x68\xe5" \
    "\x38\x71\xf3\xe5\x98\x3e\x94\x47\x86\x88\xaa\x1a" \
    "\x39\x1f\x4c\x55\xc3\x82\x59\x70\xea\x4a\x88\x91" \
    "\x21\x18\x2f\x40\x20\x40\xfa\xb6\xab\x67\xc0\x4d" \
    "\xc0\x42\x2c\xc1\xd7\x16\x2a\x30\xba\x94\x52\x99" \
    "\xe1\x3f\x14\x08\x56\x5d\xb2\xae\x4b\xaa\x14\x21" \
    "\xbc\xaa\x83\xcc\xce\xfb\xb0\x7c\x81\xae\x69\x04" \
    "\x54\xe8\xd4\x34\x8a\x6a\x23\x58\xa3\xee\x2d\xea" \
    "\xf2\x4f\x2b\x51\x10\x02\x73\xcf\x7d\x44\x7e\xb8" \
    "\x0f\xbd\x64\x63\xf9\x75\x18\xcb\x87\x84\xcf\x12" \
    "\x8e\xf6\x5d\x00\xf8\x33\x0a\xd8\x63\xf6\xd2\x1d" \
    "\x23\x79\xdc\x53\x13\x0c\x55\x5d\x0c\xc0\xd8\x9c" \
    "\xc4\x7d\x26\x43\x5e\x08\xda\x9b\x75\x8c\x55\x26" \
    "\x3d\x77\xef\x23\xfa\xa3\x7d\x6c\xc9\x3a\xe4\x1b" \
    "\x2b\x62\x73\x92\xee\x67\xcf\xd2\x31\x70\x96\xed" \
    "\x37\xee\xc4\xbb\xd4\x24\xae\x69\xa4\x47\x33\x80" \
    "\x8e\x88\xb5\xd7\xbf\x03\x62\x2a\x14\x6b\x6e\x80" \
    "\xe5\x89\x4f\xcd\x53\xa0\x50\xcc\x2e\x8d\xa9\x75" \
    "\x86\x5a\xa3\x4f\x5d\xda\x41\x76\x7f\x0a\x4d\x85" \
    "\x51\xd7\x25\xf6\xba\xc5\x8e\x63\xdb\xd0\x54\xd8" \
    "\x7a\x6b\x2f\x61\x57\x30\x24\x04\xbd\xae\xe0\xe0" \
    "\xf7\xaf\x26\x58\x2c\x52\x10\x62\x46\x54\x13\xb0" \
    "\x5f\x1d\x24\x11\x8a\xd0\xe7\x4f\xa7\x09\x74\xc1" \
    "\x62\xa7\x56\xbe\x10\x78\x7f\x46\x81\x78\x4d\xe8" \
    "\x96\x5f\x67\x28\x1a\x3d\xc7\xb3\x24\xd6\x24\x67" \
    "\xc6\x73\xe7\xa3\x66\x3b\x79\x21\x88\xa9\x30\x34" \
    "\x96\x23\xb1\xbe\x9b\x5c\x4d\x10\x57\x35\x00\xb6" \
    "\x6c\x68\xa7\x12\x6e\xc5\x58\xbb\x95\x6c\xc5\x9e" \
    "\x01\x8f\x01\xae\x2f\x94\x60\x38\xda\x32\xaf\x0c" \
    "\xb3\x10\xd4\xe6\x80\x58\x3e\x38\x76\x91\xb2\x5e" \
    "\xff\x93\xe5\x83\x06\x8d\x52\x83\x83\xfb\x77\xcf" \
    "\xe4\x54\xaf\xba\x64\x8e\xa6\x11\x3e\x64\x6b\x82" \
    "\x8e\x70\x2b\x27\x6a\x1a\xa6\x2f\x40\x13\x04\xc7" \
    "\x67\x3d\x90\xf7\xa9\x1b\xf9\xf8\xc1\xf9\x04\x4c" \
    "\x35\xb6\x74\xe1\x4a\xb3\xc7\x8b\xc4\x3b\x53\x0d" \
    "\x83\x81\xd6\xac\xd1\x7d\x6d\x27\x96\x0f\x1d\xab" \
    "\x37\xb1\x6b\xe0\x00\xbb\x32\xa7\x49\x3d\xfe\x1b" \
    "\x22\xb6\x8d\xf0\xa1\xe7\xba\x5e\x2c\xa0\xeb\x2b" \
    "\x3d\x74\x6c\x48\x42\x73\x90\x6c\xb5\x82\xc9\xac" \
    "\xb2\x16\x10\x39\xe3\xce\x27\x60\x89\xdc\xb2\x19" \
    "\x0f\x4c\xaf\xf8\xcd\x1c\xe8\x10\xd6\x75\x2c\x1f" \
    "\x7a\xef\x38\x40\xae\x54\xcf\x71\xfa\x50\x1f\xac" \
    "\xdf\x02\x6d\x06\x94\x83\x64\x2b\x15\x62\x80\xb3" \
    "\xca\xc0\xf4\x61\xd7\xa3\xb7\xe3\xa9\x71\xec\xe7" \
    "\xfb\xc1\x9f\xaf\x2c\x80\x7d\x24\xad\xcd\x33\x61" \
    "\x4c\x88\x25\x43\x0b\x14\x18\xad\xba\x24\x46\xb2" \
    "\xec\xc8\x38\x20\xca\xd0\x1a\x21\x75\x11\x24\xc2" \
    "\x03\x08\xd5\xa1\xef\xeb\x51\x7a\x1e\x3a\xc0\x03" \
    "\x3f\xee\xe2\x9e\x3b\x76\x92\x9f\xb0\x88\x76\x6e" \
    "\x27\xda\xb6\x9d\x44\x18\xa8\xd9\x38\xdf\xde\x8d" \
    "\x60\x7e\x5c\xcb\x07\xaf\xea\xaa\x30\xe7\x38\x8e" \
    "\x87\xd5\x9b\x85\x10\x2b\x4a\x73\x3e\xd2\x54\x38" \
    "\xf2\xfb\x21\xce\x1d\xfe\x05\x2d\x2b\x2f\xa2\x25" \
    "\xd4\x06\xd1\x08\xfe\x1f\x5f\x22\x57\x3c\xc9\x99" \
    "\x93\x36\xea\xe2\x1a\xfa\xdb\xe3\x14\xcf\xb9\x74" \
    "\xdd\xf0\x03\xb8\x34\x02\x1f\x09\xb2\x7b\x6e\xa1" \
    "\xff\x9e\xef\x62\x95\xc6\xe6\xc5\x2b\xf9\xf5\xea" \
    "\xa8\x36\x33\x38\x74\xd6\x1f\x9f\x49\x41\x72\x73" \
    "\x4f\xe5\x7c\x6e\xef\x0c\x87\x09\x6e\xde\x84\xfd" \
    "\x78\x96\xf2\x9e\x6f\xc2\xb1\x22\xc1\x9b\x7a\x89" \
    "\xb8\x1e\xc6\x9a\x18\x1d\x57\xa6\xb0\x54\x48\x5c" \
    "\x91\x84\x35\x1d\x78\xfb\x07\xe9\xbf\xf9\x6a\x0c" \
    "\x22\xf4\x6c\xdc\xd4\xb8\x94\xcc\xaf\x2e\x5b\x85" \
    "\xd4\xcf\x5e\x9c\x9a\xe7\x01\x7d\x63\xe2\xb9\xce" \
    "\x46\xae\xa7\xab\xa1\x5d\xd3\x10\x2b\x0d\x32\x4f" \
    "\x0f\x20\x4c\xb0\xc7\x2c\x72\xa3\xfd\xe0\x07\x31" \
    "\x1f\xea\x27\x61\xc6\x78\xe0\x7b\x5b\xb8\xf7\x91" \
    "\x61\xb4\x6b\xb6\xc0\x53\x69\x32\x47\xd3\x24\x56" \
    "\x1a\x64\xf2\x07\xc9\x8d\x66\x61\xb5\xc9\xc2\xea" \
    "\xea\xde\xb0\xc9\x61\x4d\xac\x30\x8f\x40\x60\x5d" \
    "\xe2\xb7\xc6\x4d\x3d\xe3\xed\x9a\x36\xb3\x63\xe5" \
    "\x85\x40\xe4\xf3\xe8\xba\x8e\xf6\x66\x01\x11\x8b" \
    "\xe1\x3c\x97\x61\x57\x32\x4a\x70\x75\x82\xc8\x95" \
    "\x09\xee\x7d\x64\xb8\x7e\x19\xcd\x17\xd8\xb1\x67" \
    "\x1b\xf1\xd6\x0e\x32\x56\x81\xce\xb6\x08\x79\xd7" \
    "\x85\xe3\xd6\xbc\x7d\x64\xd3\xf2\x30\xc6\x8d\xb7" \
    "\x3d\x46\x20\xf0\x1e\x2c\xbc\x13\x4e\xc9\xf5\xf6" \
    "\x13\x3d\x99\xf2\xfe\xc1\x96\x5c\xcd\x85\x46\xe9" \
    "\x98\x40\x25\x14\x66\x93\x69\xd2\x3f\x3a\x5a\xdf" \
    "\xe1\x9a\x35\x52\xed\x09\xec\x66\x9d\x70\xa9\xcc" \
    "\x40\x7e\x14\xad\x21\xf3\x3d\xd7\x6e\xe5\xc1\x67" \
    "\x06\xd1\xa0\x6e\x40\xea\xa5\x97\x6c\x6d\xc5\xbc" \
    "\xeb\xde\x97\x82\x9b\xbb\xbf\xa6\x28\x8a\xf7\x2f" \
    "\x04\x1a\x24\x3a\x79\xb9\xff\x49\xc6\xcb\x97\x78" \
    "\x47\x06\x11\xae\x43\x4e\x08\xe2\x7a\x82\x6c\x35" \
    "\x83\xe1\xcf\x9e\x7a\x85\xc6\x85\xd3\x6a\x90\x2c" \
    "\x36\xb6\x5b\x5b\xd3\x30\xc4\xf4\x11\xad\x21\x5a" \
    "\xc3\x74\x7f\x63\xc7\x87\xc4\x5a\x0f\xb1\xae\xeb" \
    "\x5b\x8a\xa2\xbc\x3b\x8d\xf7\x71\x0f\x93\x65\x8c" \
    "\xe7\xb6\xa0\x45\x6e\xe0\xd8\xc1\x2b\x38\x63\x2f" \
    "\xf6\xaa\x15\x02\x35\x81\x53\x73\x08\x0a\x81\x3d" \
    "\xe9\x60\xf8\x90\xab\x09\x0c\x5f\x90\x13\x75\x12" \
    "\x79\x5f\x60\xfa\x60\xeb\x1a\xc9\x75\x09\x44\x7b" \
    "\xfb\xdf\x82\xeb\x53\x87\xf1\x9d\x5f\xb2\x22\x9a" \
    "\x53\x14\xe5\xc3\xb9\x58\xe7\x25\x30\x87\x88\x02" \
    "\xac\xa2\xe8\x6c\xa5\xd9\x4d\x71\x2a\xdb\x4a\x28" \
    "\xa6\xd4\xdf\x07\x61\xb0\xf3\xd0\x62\x80\x9d\x03" \
    "\xcd\x80\x52\x1e\x96\xb7\x83\xce\x39\xae\xec\x7e" \
    "\x19\x51\xfe\x15\x2b\xe3\x87\x15\x45\x71\x3f\x0e" \
    "\xe3\x13\x09\x2c\x20\xd3\x84\x47\x27\xa7\xb2\x29" \
    "\x74\x63\x3d\x95\x13\xcb\x09\x45\x17\x53\x29\x40" \
    "\x38\x2e\xa9\x16\x26\x09\x77\xfc\x89\x9a\x3d\x8c" \
    "\xd9\x91\x06\x4e\x4d\x3f\x3e\x3e\xa9\xfd\xc7\x04" \
    "\xe6\x10\x81\x73\xa8\x34\xb1\x84\x49\x82\xb4\xa0" \
    "\x32\xc9\x14\x2d\x38\xc0\x07\x8a\xa2\x7c\xf4\xdf" \
    "\xc6\xfc\x9f\xb6\x7f\x02\x9e\xde\x3f\x78\x85\xa5" \
    "\x79\x67\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42" \
    "\x60\x82"

class WelcomeDlg(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("WelcomeDlg")

        self.setIcon(self.image0)


        self.welcomeLabel = QLabel(self,"welcomeLabel")
        self.welcomeLabel.setGeometry(QRect(170,60,420,160))
        self.welcomeLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.welcomePixmap = QLabel(self,"welcomePixmap")
        self.welcomePixmap.setGeometry(QRect(-5,0,142,290))
        self.welcomePixmap.setScaledContents(1)

        self.languageChange()

        self.resize(QSize(619,287).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Feedback Wizard"))
        self.welcomeLabel.setText(i18n("<h2>Welcome to Pardus</h2>\n"
"\n"
"With this small wizard, you can send your messages to Pardus \n"
"developers and help Pardus be the best Linux in the world.\n"
"\n"
"<p>\n"
"The information you will give here will accelerate Pardus development. \n"
"Please click on \"Forward\" button for the next step.\n"
"<p>"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'questiondlg.ui'
#
# Created: Paz Tem 9 09:41:15 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20060407
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *


image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x20\x00\x00\x00\x20" \
    "\x08\x06\x00\x00\x00\x73\x7a\x7a\xf4\x00\x00\x08" \
    "\x58\x49\x44\x41\x54\x58\x85\xe5\x97\x61\x4c\xd4" \
    "\xe7\x1d\xc7\x3f\xb7\x9e\xcd\xff\x5a\xa9\x87\x71" \
    "\xcd\x99\xd0\xe4\xd8\x68\xc2\xd9\x33\x41\xa3\x8b" \
    "\x50\xb6\x09\xe9\x16\x8b\x75\x51\x88\x2f\x7a\x37" \
    "\xd7\xec\x98\x4d\x94\x35\x5d\x03\xed\xe2\x94\x2d" \
    "\x1d\x2e\x8b\x11\xda\x98\x71\x6d\xba\x70\x74\xae" \
    "\xa0\xc9\x7a\xd0\xb4\x45\xba\xb8\x82\x9d\x9b\xe7" \
    "\x22\x0a\xc4\x09\x38\xed\xee\xba\x6a\x80\x74\x1d" \
    "\x47\x95\xdc\x3d\xc5\xff\xfc\xee\xc5\xff\x44\xb1" \
    "\x74\x6e\xaf\xf6\x62\xcf\x9b\x5f\x9e\xe7\x9f\xfc" \
    "\x7e\xdf\xe7\xfb\xfd\xfe\x9e\xe7\xf9\xc3\xff\xfb" \
    "\x70\x2d\xb4\x28\xe9\x0b\xc0\xd7\x78\x3b\xba\x0a" \
    "\x7f\xd5\x22\x86\x62\x10\xa8\x86\x81\x18\x04\xc2" \
    "\x30\x10\x85\x07\x43\x30\xd4\x0e\x45\xd5\x70\x3a" \
    "\x06\xc5\x61\x18\x8e\x41\x31\x30\x6c\x20\x18\x82" \
    "\xe1\x76\x08\xc2\xe8\x64\xe1\x27\x2b\x9e\x3f\xf2" \
    "\x5b\xd7\x52\xd7\xdf\xee\x08\x40\x67\xfb\x1e\x64" \
    "\xf1\xaa\x76\x4e\x46\x1f\x66\x6d\xad\x8b\xe1\x18" \
    "\x94\x58\x4e\xd2\x92\x5a\x38\x17\x83\xa0\x05\xe7" \
    "\x80\x60\xf8\xe6\xfc\xdf\x7d\x4f\x1b\x52\x1f\x8c" \
    "\x65\x0b\xa7\xcd\x01\x1a\x5b\x7f\xec\xba\xff\x4b" \
    "\xd7\x16\x04\xa0\x0f\x47\x7c\xd8\xcb\xff\xc8\xe9" \
    "\xe8\x97\x29\xaa\x86\x3f\x44\x21\x50\x93\xdb\x79" \
    "\x35\x0c\xb4\x43\x51\x08\x4e\x47\x9d\x22\xa7\x8d" \
    "\x53\xe4\x74\x0c\x82\x90\x18\x36\x94\x05\x43\x30" \
    "\x74\x08\x80\x23\x76\x96\x8d\xee\x5a\xc8\xeb\x86" \
    "\xc7\x9b\x21\xd5\x2b\xdc\xab\x7e\xc1\x93\xe1\xa7" \
    "\x5d\x2e\xd7\x02\x00\xc6\x33\x2f\x72\xac\xe5\x07" \
    "\x4c\x4f\x90\x9d\x99\xc6\x63\x0c\x59\x63\xf0\xd8" \
    "\xd9\xdc\x1c\xb2\x33\x69\x3c\xd7\x20\x65\x0c\x85" \
    "\x58\x24\x8c\xa1\xcc\x86\x23\xb6\x61\xa3\x0d\x31" \
    "\xdb\x50\x0b\x44\x6d\x43\xc4\x6d\xd1\x6e\x1b\x42" \
    "\x40\xcc\x86\x86\xb5\xa5\xa4\xfc\xcb\xed\xc2\x65" \
    "\x4d\x6b\x5d\x4f\x3f\x34\x0c\xf0\x85\x5b\x74\x77" \
    "\x71\xba\x7d\x0b\x85\x55\x60\x0c\x9e\xb5\x75\xf0" \
    "\x68\x04\xcf\x8e\x38\x58\xf9\x78\x8a\x6b\x9d\xf5" \
    "\x6b\x1e\xb0\xa1\xb0\xb4\x1e\x0a\x57\x50\xb6\xbd" \
    "\x8d\xc1\x07\x96\xb3\xd1\x6d\xd1\x69\x1b\x6a\xdd" \
    "\x16\x31\x20\xe2\xb6\xe8\x0f\xac\xa2\xee\xa5\x24" \
    "\x63\x5b\x77\x52\xeb\xb6\x68\x1e\x38\x49\xa1\x2f" \
    "\xed\x4e\xfc\xe9\xdb\x5b\x16\x32\xde\x3d\xea\x4c" \
    "\x66\x33\x07\x22\xd2\x81\x88\x34\x9e\x94\xae\x48" \
    "\x1a\xec\x93\x24\xe9\x78\x5c\x8a\x9e\x51\xa6\xb7" \
    "\xcd\x99\x67\x32\x4e\xb8\xf1\xfd\xa3\x71\xe9\x8a" \
    "\x34\x72\xa0\x5e\xda\x15\x51\x66\xf0\x84\x24\xe9" \
    "\x4c\x4b\xbd\x13\xf7\xd5\x6b\xbc\x18\xb5\x06\x2d" \
    "\x69\x5b\xe9\xab\x0b\x01\x58\xa6\x57\xea\x6d\x1d" \
    "\xed\x93\xfa\x3b\x9c\xa4\xcf\x56\x48\xaf\xb4\x4a" \
    "\xcf\x56\xe5\x8a\x48\xba\x90\x91\x1a\x43\xd2\xbe" \
    "\x52\xf5\x95\xfb\xa4\x72\x9f\xe2\x6b\xbc\xd2\x63" \
    "\x01\x9d\xd9\x15\x92\x2e\x48\x9a\x95\x74\x6a\x5c" \
    "\xad\x41\x4b\x53\x41\x4b\x1d\x8f\xf8\x25\x49\xad" \
    "\xeb\x7c\x1a\x2f\x46\xf1\xcd\x81\xf8\x8d\xba\x73" \
    "\x12\x70\x35\x9d\x87\xc9\xba\xb2\x03\x31\xf0\x55" \
    "\x42\x6a\x10\x6c\xc8\x0e\xc7\xc0\x6d\xc1\xd5\x34" \
    "\x18\xc0\x0c\xc1\xf9\x21\x26\x0a\xaa\xa9\x04\xba" \
    "\x8c\xa1\x06\x88\x5d\x4e\x11\x78\xa7\x9b\x68\xb5" \
    "\x0b\x5e\x1e\x25\x6d\x06\x09\x61\x88\xd9\x86\xb0" \
    "\xe5\x21\x7b\x71\x90\xd0\xcc\x34\x31\x1b\x6a\x66" \
    "\xb2\x4b\x24\xdd\x06\x20\x2f\x7f\x31\xc6\xb8\x3c" \
    "\x2b\x43\x70\xf8\xfb\x50\xb8\x1a\x36\xd5\xe1\x09" \
    "\x5a\xb0\xa5\x0e\x3e\xb6\xe0\xd5\x5a\xb0\x0b\x49" \
    "\xa4\xd3\x2c\x7f\x2d\xca\x11\xdb\x50\xe3\x66\x4e" \
    "\xfb\x43\xb6\xa3\x7d\xec\xb5\x87\xc9\xff\xea\x46" \
    "\x12\x6b\x2b\x68\xf0\x07\xe0\x85\x38\x9e\x73\x86" \
    "\xa8\x31\x84\x81\x4e\x63\xbc\x9f\x39\x02\x74\xb6" \
    "\xaf\x5c\x3f\x0b\x5d\xcf\x34\x56\x49\xbb\xaa\x94" \
    "\xd9\x17\x71\x68\xbf\x32\x25\x49\x9a\x6a\x0c\x39" \
    "\x5a\x6e\xf0\x4b\xfb\x76\xaa\x67\x9d\x57\x5a\xe7" \
    "\x55\x47\x89\x25\x95\x58\x6a\x0b\x5a\xca\x94\x58" \
    "\x6a\x0d\xa2\xa9\x20\x3a\xb1\x2b\x74\xd3\x2b\x19" \
    "\x69\x7f\x31\x4a\x16\xa1\xa6\x22\x94\x29\xf7\xff" \
    "\x45\x57\xa6\xee\x9a\xcf\x40\x41\xe5\x52\x6c\xe3" \
    "\xf2\xac\x8c\x80\xc9\xe2\xf1\x8e\xc1\xef\x3a\x21" \
    "\x2f\x1f\x7e\xdd\x4c\xfe\x50\x82\xd1\x2d\x2b\x58" \
    "\x6d\x03\xef\x74\xe7\x5c\x0f\xe1\x9c\xeb\x43\x6e" \
    "\x72\x2d\xe7\x30\x11\x78\xa7\x1b\x2e\x0e\x82\xc7" \
    "\x43\x67\xf5\x0a\x67\xe7\x40\x18\x68\xc7\xdc\x4b" \
    "\x5e\xbe\x6b\x3e\x80\xf7\xa2\xf7\x71\x79\x82\x23" \
    "\xbf\x6c\x20\x7b\x6c\x88\xbd\x3f\x3f\x09\xaf\x77" \
    "\x93\xbd\x94\x22\xd5\xd4\xc8\x9e\x73\x1f\xd0\x7b" \
    "\x3e\x45\x74\x72\x12\x66\x0c\x5d\xb6\x43\xe7\x8d" \
    "\xbe\x3f\x94\x6b\xbd\x43\xb6\x21\xe4\x86\x98\x31" \
    "\xf0\x62\x23\xfc\x7d\x82\xca\xcb\x29\x62\xb6\x53" \
    "\x26\x66\x43\xc8\xe6\x5e\xde\x68\xbe\x6b\xbe\x04" \
    "\x07\x3a\x76\xd6\x17\xa0\x11\x3f\xba\x11\xf5\x56" \
    "\x87\xd4\x79\x42\xf5\x05\x68\x3c\xe8\x55\x7c\xf3" \
    "\x2a\xa9\x7f\x44\x3a\x1a\x77\x5c\xbd\xc6\xab\x4c" \
    "\x89\xa5\x33\x8d\x21\xc7\xf9\x83\x92\x0e\xf6\xa8" \
    "\x67\x73\x40\x53\x25\x96\xf6\x17\x23\x49\x8a\x6f" \
    "\xab\x98\xa3\x3f\x59\x84\x5a\x83\x96\xd1\x87\xba" \
    "\x0f\xc0\x7d\x03\x40\xd7\xb1\x96\xfb\x22\x6e\x68" \
    "\xb7\xc1\xca\xc5\xe6\xf2\x30\x9d\x75\x65\x58\x6e" \
    "\x68\x99\x9e\x26\x32\x3c\x44\xc3\x77\x1e\xc2\x72" \
    "\x43\x68\x47\x3d\x55\xd3\x86\x46\x63\x68\x9e\x36" \
    "\x74\x3d\xb1\x9a\xca\xb1\x31\x67\xe7\xc0\x58\x8e" \
    "\xee\xd4\xdb\x31\x6a\x96\x2d\x67\xaf\x0d\x61\xb7" \
    "\xc3\x80\xd7\x70\x77\xfa\xfd\x23\xf7\x00\x57\xe6" \
    "\x24\xa8\x99\x31\xde\x76\x1b\x22\x6e\x30\xb9\xc8" \
    "\xbb\x31\xc2\x1b\xf6\xce\xcd\x6f\xfd\xbe\xa2\xa2" \
    "\x8e\xa8\x31\x44\xdc\x10\x1d\x48\x50\xb3\xb5\x95" \
    "\xe8\x8c\xd3\x0d\x00\x0d\xdb\x4a\xe9\xf5\xf9\x29" \
    "\xdc\x54\x4b\xd7\x64\x6a\xae\x78\x2d\x30\x6d\x1b" \
    "\x57\x7e\xc9\xc6\xbc\x79\x1e\x88\x41\xbe\x75\x4b" \
    "\x91\x76\x1b\x48\x8d\x31\x68\x06\x89\x90\x63\x06" \
    "\x72\xad\x06\x5d\x2f\x86\x21\xb7\x5e\xf1\xf1\x34" \
    "\x9d\x87\x1b\x30\x36\xb4\xcc\x18\xea\x7c\x7e\x8e" \
    "\xbc\x6f\x11\xb2\x0d\xa4\xd3\x54\x5e\xbc\xe9\x81" \
    "\xa8\xe3\x01\x26\xde\x6d\xce\x9b\xe7\x81\xcc\x86" \
    "\xfd\x87\x6f\xf7\x40\x7c\x5b\x95\x74\x45\x73\xf3" \
    "\xa6\x62\x4b\xda\x57\xa1\xfa\x02\xa4\x58\x8f\xe3" \
    "\x85\x8f\x24\x1d\x8d\x6b\x6a\x8d\xcf\x59\x8f\x76" \
    "\xa8\x75\xbd\x5f\xea\x4f\x4a\xcf\xef\x94\x24\xed" \
    "\xf6\xcf\xcf\x5b\x5f\x80\xd4\x19\xff\xfa\x3c\x06" \
    "\xda\x4d\x74\xc9\x9c\x07\x72\x3b\x2b\xfb\x73\x02" \
    "\xcc\x04\x3e\xaf\x97\x76\x1b\xf6\x3c\x95\xa4\xf3" \
    "\xb4\xa3\x71\xf3\xcb\xdf\x83\x6f\xd4\xc0\x17\x81" \
    "\x89\x4a\x5a\x26\x27\x89\x00\xa3\xde\x69\x42\x36" \
    "\x34\xff\xa8\x0c\xdc\xb5\xa4\xde\x88\x81\x7d\x1b" \
    "\xb3\x40\xea\xb5\x06\x6b\x3e\x03\xeb\x7c\xbf\xbf" \
    "\x9d\x81\xfa\x02\xa4\xa3\x23\xd2\x87\x72\x2e\xa6" \
    "\x59\x49\xc7\xc7\xa5\xa7\xaa\xa5\x7d\x15\x6a\x7d" \
    "\x24\x20\x8d\xcb\x61\xe6\x60\x8f\xfa\x76\x54\x3b" \
    "\x87\xcf\x59\x27\x28\x39\x22\x3d\xd6\xaa\x05\xf3" \
    "\xae\xf1\x6e\x04\x98\xeb\xc5\xe5\x3e\xf7\x93\xc6" \
    "\x98\x07\x06\x6e\x41\x6a\xb9\xa1\xf7\x8d\x97\x58" \
    "\xf9\xe6\x2b\xcc\x2c\xf7\x90\xb7\xf2\x2b\xb0\xd4" \
    "\x86\x53\xc7\xe9\x1a\x38\xcf\xa5\xf3\x29\xdc\xb3" \
    "\x29\x2a\x2f\x5c\xe4\x68\x7a\x8c\x8d\x3f\x7c\x13" \
    "\x16\xdb\x70\xff\x22\xfa\x77\x85\x89\xed\x7e\x86" \
    "\xde\xcb\x6f\xcd\xcb\x37\x60\x43\x08\xe8\x5f\xcc" \
    "\xa1\xee\x71\xfb\xe2\x9c\x04\x75\xdb\xdb\x26\x17" \
    "\x72\x7b\xbd\xcf\x47\x6a\x53\x15\xde\x97\xd2\xf0" \
    "\x5c\x18\x2e\x5b\xb0\xbd\x9e\xaa\xe9\x2c\x85\x25" \
    "\xab\x28\xdb\xda\x4c\xcc\x0d\x35\x9b\xf7\x82\xcf" \
    "\x03\xef\x8d\x11\xfb\xd6\x6a\x2a\x7d\x55\xec\x7d" \
    "\xb4\x2a\xf7\x28\x99\xdf\x5d\xdd\x6e\x08\xff\x66" \
    "\x2a\x33\x5f\x82\x53\x7d\xdf\x1d\x0f\x7a\x55\x5f" \
    "\x80\x76\xe7\x68\x4a\x16\x59\x8a\x3f\x5e\xaa\xdd" \
    "\x7e\xd4\xb7\xa3\x5a\x99\xf5\x01\x9d\x68\x8c\x48" \
    "\x57\xa4\xa9\x44\x9f\xb4\x6b\xa7\x9a\x82\x5e\x69" \
    "\x34\xa3\x4c\x32\x29\xb5\x8c\x28\xbe\xad\x42\x7a" \
    "\xaa\x5a\xad\xe5\x7e\x25\x83\x5e\x75\x3c\xb6\x6a" \
    "\x2e\xdf\x1c\xfd\xdb\xab\xa6\x94\xc9\x2c\x99\x7f" \
    "\x12\x4a\x9e\x91\x03\xbb\x2f\x24\x8b\xac\xcf\xb8" \
    "\x76\x7f\x89\x57\x99\x72\xbf\xfa\x9e\x09\x69\xbc" \
    "\xc4\xa7\xfd\x41\xaf\xa3\x71\x6f\x5c\x3a\x9b\x91" \
    "\x46\x25\xf5\x27\x73\x5d\x10\x57\x6b\xb9\x5f\x7a" \
    "\xbe\x74\x41\xed\xa7\xd6\xf9\xa4\x44\xcf\x4f\x6f" \
    "\x5c\xc7\xae\xdb\x40\x94\xa7\x5e\xa8\xeb\xf5\x1d" \
    "\x3e\x94\x17\x9d\x99\x06\x1c\xda\xc2\x40\xef\x32" \
    "\x1f\x75\x81\x00\x7b\x8e\x1d\x23\x04\x74\x2f\xb6" \
    "\xd8\x53\x5a\x49\xff\x62\x2f\x95\x97\x27\x68\x38" \
    "\x79\x0c\x2b\x47\x73\xf3\xd6\x10\x0d\xaf\x1f\xc2" \
    "\xc2\x79\x42\x44\x80\x76\xa0\xc9\xef\xc7\x3c\xb7" \
    "\xe7\x78\xfe\xa6\xda\x0d\x2e\x97\x2b\xcb\x42\x43" \
    "\x52\x85\x8e\xb6\xbd\xaf\xee\x1e\x69\x73\x40\x5a" \
    "\xef\x73\xae\xde\x0d\x4d\xea\x58\x73\xeb\x95\xeb" \
    "\x9c\xf5\xe3\xc5\x37\xcf\xf8\x26\xbf\x13\xf7\x07" \
    "\x2d\x25\x8b\x2c\xed\x2e\x40\x23\x7e\x4b\x6d\xeb" \
    "\xfd\xd2\x5b\x27\x6c\x9d\xea\x79\x5d\xd2\xd2\x5b" \
    "\xeb\x7d\xde\x8f\xc9\x12\x2e\x26\x6a\xf0\x97\x3d" \
    "\x41\x4f\xf3\x3a\x2e\xa5\xee\xce\x7e\x3c\x89\x67" \
    "\xc6\x90\x9e\x49\x93\x6f\x0c\xa9\xab\x69\x0a\x6d" \
    "\x48\xcc\x18\xca\x6c\x43\x97\xc1\x79\x19\xd9\x86" \
    "\x90\x0d\xdd\x5e\x8b\xf0\xda\x4a\xd2\xa5\xa5\xff" \
    "\xc8\xdf\xda\xf0\x26\x97\x46\x7f\xc5\x03\x2b\x12" \
    "\x2e\x97\xeb\x9f\x0b\xee\xfc\x73\x80\xb8\x24\x05" \
    "\x34\xaa\x26\xcd\x2a\xa9\xfe\xb6\xeb\xfa\x48\x52" \
    "\x6f\x9b\x74\x61\x5c\x3a\xb8\x5b\x4a\x9c\x91\x5a" \
    "\x22\x52\x77\x8f\xb4\xab\xca\x89\x9d\x4d\xb3\x9a" \
    "\x55\xbf\x2e\x9c\x79\x42\x92\xf7\x3f\x2e\x78\x07" \
    "\x30\x8b\x24\x7d\x53\x67\xfb\x0e\x6a\x56\x7f\xd5" \
    "\xa9\x9e\x4f\x95\x91\x94\x88\x4b\x19\x5d\xd7\xa9" \
    "\xf8\x27\x9a\xd5\x29\x8d\x9e\xf8\x89\xa4\xa2\x1b" \
    "\x26\xbb\xd3\x58\x50\x82\x3b\x00\x81\x6b\xb8\x59" \
    "\xc4\xbd\x5c\x25\x9f\x3c\xdc\x5c\x25\x43\x1e\x69" \
    "\xe0\x53\x97\xcb\x75\xfd\xbf\xcd\xf9\x3f\x1d\xff" \
    "\x02\xb7\x44\x8e\x02\xf0\x2d\xe1\x4f\x00\x00\x00" \
    "\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

class QuestionDlg(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("QuestionDlg")

        self.setIcon(self.image0)


        self.buttonGroup = QButtonGroup(self,"buttonGroup")
        self.buttonGroup.setGeometry(QRect(170,130,400,110))

        self.questionOne = QRadioButton(self.buttonGroup,"questionOne")
        self.questionOne.setGeometry(QRect(21,15,343,19))
        self.questionOne.setChecked(1)
        self.buttonGroup.insert( self.questionOne,0)

        self.questionTwo = QRadioButton(self.buttonGroup,"questionTwo")
        self.questionTwo.setGeometry(QRect(21,45,343,19))
        self.buttonGroup.insert( self.questionTwo,1)

        self.questionThree = QRadioButton(self.buttonGroup,"questionThree")
        self.questionThree.setGeometry(QRect(21,75,343,19))
        self.buttonGroup.insert( self.questionThree,2)

        self.questionLabel = QLabel(self,"questionLabel")
        self.questionLabel.setGeometry(QRect(170,60,420,40))
        questionLabel_font = QFont(self.questionLabel.font())
        self.questionLabel.setFont(questionLabel_font)
        self.questionLabel.setTextFormat(QLabel.RichText)
        self.questionLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.stepLabel = QLabel(self,"stepLabel")
        self.stepLabel.setGeometry(QRect(160,20,100,21))
        self.stepLabel.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel.setFrameShape(QLabel.NoFrame)
        self.stepLabel.setFrameShadow(QLabel.Plain)

        self.questionPixmap = QLabel(self,"questionPixmap")
        self.questionPixmap.setGeometry(QRect(-5,0,142,290))
        self.questionPixmap.setScaledContents(1)

        self.languageChange()

        self.resize(QSize(619,287).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Feedback Wizard"))
        self.buttonGroup.setTitle(QString.null)
        self.questionOne.setText(i18n("Very satisfying. Pardus fulfils my requirements"))
        self.questionTwo.setText(i18n("Good, however it lacks some capabilities"))
        self.questionThree.setText(i18n("It does not meet my requirements"))
        self.questionLabel.setText(i18n("<h2>How does Pardus fit your needs?</h2>"))
        self.stepLabel.setText(i18n("<b>Step 4 of 7</b>"))


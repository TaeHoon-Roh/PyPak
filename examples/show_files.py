#!/usr/bin/env python

#
# Example program for listing the files on a data logger
#
# Update the file pakbus.conf to your local settings first!
#

#
# (c) 2009 Dietrich Feist, Max Planck Institute for Biogeochemistry, Jena Germany
#          Email: dfeist@bgc-jena.mpg.de
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import socket
import sys
import os
import string
import datetime
import examples.pakbus as pakbus
from examples.bintools import str2int

# make func
City = ['YangYang', 'Buan', 'Seoul', 'Daegu', 'Jeju']


def makeFilePath(filename, lastupdate):
    year = lastupdate.year
    month = lastupdate.month
    temp = str(filename)
    filepath = '/home/uxfac/rawData/' + str(City[0]) + '/' + str(year) + '/' + str(month)
    print("check FilePath : ", filepath)
    if '1hr' in temp:
        filepath = filepath + '/' + '1hr'
    elif '1min' in temp:
        filepath = filepath + '/' + '1min'
    elif '1sec' in temp:
        filepath = filepath + '/' + '1sec'
    elif '10min' in temp:
        filepath = filepath + '/' + '10min'
    else:
        filepath = ''

    if filepath != '':
        if not os.path.exists(filepath):
            os.makedirs(filepath)
    return filepath

def makeFileName(filename, lastupdate):
    year = lastupdate.year
    month = lastupdate.month
    day = lastupdate.day
    lastFileName=''
    if '1hr' in filename:
        lastFileName = City[0]+'.'+'1hr'+'.'+str(year)+'-'+str(month)+'-'+str(day)+'.dat'
    if '1min' in filename:
        lastFileName = City[0] + '.' + '1min' + '.' + str(year) + '-' + str(month) + '-' + str(day) + '.dat'
    if '1sec' in filename:
        lastFileName = City[0] + '.' + '1sec' + '.' + str(year) + '-' + str(month) + '-' + str(day) + '.dat'
    if '10min' in filename:
        lastFileName = City[0] + '.' + '10min' + '.' + str(year) + '-' + str(month) + '-' + str(day) + '.dat'
    return lastFileName


#
# Initialize parameters
#

# Parse command line arguments
import optparse

parser = optparse.OptionParser()
parser.add_option('-c', '--config', help='read configuration from FILE [default: %default]', metavar='FILE',
                  default='pakbus.conf')
(options, args) = parser.parse_args()

# Read configuration file
import ConfigParser, StringIO

cf = ConfigParser.SafeConfigParser()
print ('configuration read from %s' % cf.read(options.config))

# Data logger PakBus Node Id
NodeId = str2int(cf.get('pakbus', 'node_id'))
# My PakBus Node Id
MyNodeId = str2int(cf.get('pakbus', 'my_node_id'))

# Open socket
s = pakbus.open_socket(cf.get('pakbus', 'host'), cf.getint('pakbus', 'port'), cf.getint('pakbus', 'timeout'))

# check if remote node is up
# msg = pakbus.ping_node(s, NodeId, MyNodeId)
# if not msg:
#     raise Warning('no reply from PakBus node 0x%.3x' % NodeId)

#
# Main program
#

# Upload directory data
FileData, Response = pakbus.fileupload(s, NodeId, MyNodeId, '.DIR')

# List files in directory
# now = datetime.datetime.now()
now = datetime.datetime.now()
flag = now + datetime.timedelta(days=-1)

filedir = pakbus.parse_filedir(FileData)
for file in filedir['files']:
    print ("File Name : ", file['FileName'])
    last = str(file['LastUpdate'])
    if len(last) == 0:
        continue
    print (last)
    lastupdate = datetime.datetime.strptime(last, '%Y-%m-%d %H:%M:%S')
    if lastupdate > flag:
        filepath = makeFilePath(file['FileName'], lastupdate)
        if filepath != '':
            filename = filepath+"/"+makeFileName(file['FileName'], lastupdate)
            FileData, Response = pakbus.fileupload(s, NodeId, MyNodeId, file['FileName'])
            f = open(filename, 'w')
            f.write(FileData)
            f.close()
        else:
            continue


print (now, flag)

# print("hihihihihihihihihihihi")

# FileData, Response = pakbus.fileupload(s,NodeId, MyNodeId, 'CRD:YangYang.10min_data_30.dat')
# print FileData

# if not os.path.exists("/home/uxfac/newfile"):
#    os.makedirs("/home/uxfac/newfile")
# f = open("/home/uxfac/newfile/"+file['FileName'],'w')
# f.write(FileData)
# f.close()

# say good bye
pakbus.send(s, pakbus.pkt_bye_cmd(NodeId, MyNodeId))

# close socket
s.close()

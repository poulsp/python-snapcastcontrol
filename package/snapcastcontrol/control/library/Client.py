#  Copyright (c) 2021
#
#  This file, Client.py, is part of Project python-SnapControl.
#
#  Project python-SnapControl is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>


from .Host import (Host)


#-----------------------------------------------
class Client():
  def __init__(self, clientData):
    # print(f"######################## Client created")

    self._id = clientData['id']
    self._connected = False

    self._host = Host(clientData['host'])
    snapclient = clientData['snapclient']
    self._snapclient = {
      'name': snapclient['name'],
      'protocolVersion': snapclient['protocolVersion'],
      'version': snapclient['version']
    }

    config = clientData['config']
    self._config = {
      'instance': config['instance'],
      'latency': config['latency'],
      'name': config['name'],
      'volume': {
        'muted': config['volume']['muted'],
        'percent': config['volume']['percent']
      }
    }

    self._name = self._host.name if self._config['name'] == "" else self.config['name']

    self._volumeLevel = self._config.get('volume').get('percent')
    self._muted = self._config.get('volume').get('muted')
    self._latency = self._config.get('latency')

    self._lastSeen = clientData['lastSeen']
    self._connected = clientData['connected']


  #-----------------------------------------------
  @property
  def id(self):
    return self._id

  #-----------------------------------------------
  @property
  def name(self):
    return self._name

  #-----------------------------------------------
  @name.setter
  def name(self, value):
    self._name = value

  #-----------------------------------------------
  @property
  def volumeLevel(self):
    return self._volumeLevel

  #-----------------------------------------------
  @volumeLevel.setter
  def volumeLevel(self, value):
    self._volumeLevel = value

  #-----------------------------------------------
  @property
  def muted(self):
    return self._muted

  #-----------------------------------------------
  @muted.setter
  def muted(self, value):
    self._muted = value

  #-----------------------------------------------
  @property
  def host(self):
    return self._host

  #-----------------------------------------------
  @property
  def config(self):
    return self._config

  #-----------------------------------------------
  @property
  def lastSeen(self):
    return self._lastSeen

  #-----------------------------------------------
  @property
  def connected(self):
    return self._connected

  #-----------------------------------------------
  @connected.setter
  def connected(self, value):
    self._connected = value

  @property
  def latency(self):
    return self._latency

  #-----------------------------------------------
  @latency.setter
  def latency(self, value):
    self._latency = value


  # #-----------------------------------------------
  # def __repr__(self):
  #   rep = f'Client(id:{self._id}, name:{self._name}, volumeLevel:{self._volumeLevel}, muted:{self._muted}, latency:{self._latency})'
  #   return rep


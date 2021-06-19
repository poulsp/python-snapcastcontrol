#  Copyright (c) 2021
#
#  This file, Group.py, is part of Project python-SnapControl.
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


from .Client import (Client)


#-----------------------------------------------
class Group():
  def __init__(self, groupData):
    # print(f"######################## Group created")

    self._name = groupData['name']
    self._id = groupData['id']
    #TODO kald den stream_id eller streamId??
    self._stream_id = groupData['stream_id']
    self._muted = False

    self._clients = []
    for client in groupData['clients']:
      self._clients.append(Client(client))


  #-----------------------------------------------
  def getClient(self, id):
    for client in self._clients:
      if client.id == id:
        return client


#-----------------------------------------------
  def getClients(self):
    return self._clients


  #-----------------------------------------------
  @property
  def clients(self):
    return self._clients

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
  def muted(self):
    return self._muted

  #-----------------------------------------------
  @muted.setter
  def muted(self, value):
    self._muted = value

  #-----------------------------------------------
  @property
  def stream_id(self):
    return self._stream_id

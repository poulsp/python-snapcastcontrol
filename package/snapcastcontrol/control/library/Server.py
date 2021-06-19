#  Copyright (c) 2021
#
#  This file, Server.py, is part of Project python-SnapControl.
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


from .Host   import (Host)
from .Group  import (Group)
from .Stream import (Stream)


#-----------------------------------------------
class Server():
  def __init__(self, serverData):
    # print(f"######################## Server created")
    self._groups = []
    self._streams = []


    snapserver = serverData.get('server').get('snapserver')
    host = serverData.get('server').get('host')

    for group in serverData.get('groups'):
      self._groups.append(Group(group))

    self.server = {
       'host': Host(host),
       'snapserver': {
          'controlProtocolVersion': snapserver.get('controlProtocolVersion'),
          'name': snapserver.get('name'),
          'protocolVersion':  snapserver.get('protocolVersion'),
          'version': snapserver.get('version')
        }
     }

    for stream in serverData.get('streams'):
        self._streams.append(Stream(stream));


  #-----------------------------------------------
  @property
  def groups(self):
    return self._groups


  #-----------------------------------------------
  @property
  def streams(self):
    return self._streams


  #-----------------------------------------------
  def getClient(self, id):
    for group in self._groups:
      client = group.getClient(id)
      if client:
        return client


  #-----------------------------------------------
  def getClients(self):
    clientsArr = []
    for group in self._groups:
      clients = group.getClients()
      for client in clients:
        clientsArr.append(client)

    return clientsArr


  #-----------------------------------------------
  def getGroup(self, id):
    for group in self._groups:
      if (group.id == id):
        return group


  #-----------------------------------------------
  def getStream(self, id):
    for stream in self._streams:
      if stream.id == id:
        return stream


  #-----------------------------------------------
  def getStreams(self):
    for stream in self._streams:
      print(f"stream.id: {stream.id} ")


#  Copyright (c) 2021
#
#  This file, SnapControlProtocol.py, is part of Project python-SnapControl.
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


import asyncio
import json
import random


SERVER_ONDISCONNECT = 'Server.OnDisconnect'
ONMESSAGE = 'onMessage'


#-----------------------------------------------
def jsonrpcRequest(method, id, params=None):
  return (json.dumps({
                      'id': id,
                      'jsonrpc':  '2.0',
                      'method': method,
                      'params': params or {}
                      }
                    ) + "\r\n").encode()


#-----------------------------------------------
class SnapControlProtocol(asyncio.Protocol):

  #-----------------------------------------------
  def __init__(self, callbacks):
    self._transport = None
    self._buffer = {}
    self._callbacks = callbacks
    self._data_buffer = ''


  #-----------------------------------------------
  # BaseProtocol.connection_made(transport)
  def connection_made(self, transport):
    self._transport = transport


  #-----------------------------------------------
  # BaseProtocol.connection_lost(exc)
  def connection_lost(self, exception):
    self._callbacks.get(SERVER_ONDISCONNECT)(exception)


  #-----------------------------------------------
  # Protocol.data_received(data)
  def data_received(self, data):
    self._data_buffer += data.decode()
    if not self._data_buffer.endswith('\r\n'):
      return

    data = self._data_buffer
    self._data_buffer = ''
    for cmd in data.strip().split('\r\n'):
      data = json.loads(cmd)
      if not isinstance(data, list):
        data = [data]
      for item in data:
        if 'id' in item: # response from request
          # print(f"response")
          id = item.get('id')
          self._buffer[id]['data'] = item
          self._buffer[id]['event'].set()

        else: # notification
          # print(f"notification")
          self._callbacks.get(ONMESSAGE)(item)


  #-----------------------------------------------
  async def request(self, method, params):
    id = random.randint(1, 1000)

    # send request
    self._transport.write(jsonrpcRequest(method, id, params))

    # response
    self._buffer[id] = {'event': asyncio.Event() }
    await self._buffer[id]['event'].wait()
    response = self._buffer[id]['data']
    del self._buffer[id]
    #self._buffer = {}

    return response

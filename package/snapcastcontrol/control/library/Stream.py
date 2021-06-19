#  Copyright (c) 2021
#
#  This file, Stream.py, is part of Project python-SnapControl.
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


#-----------------------------------------------
class Stream():
  def __init__(self, streamData):
    # print(f"######################## Stream created ")

    self._id = streamData['id']
    self._status = streamData['status']

    uri = streamData['uri']
    self._uri = {
      'raw': uri['raw'],
      'scheme': uri['scheme'],
      'host': uri['host'],
      'path': uri['path'],
      'fragment': uri['fragment'],
      'query': uri['query']
    }


  #-----------------------------------------------
  @property
  def id(self):
    return self._id

  #-----------------------------------------------
  @property
  def status(self):
    return self._status

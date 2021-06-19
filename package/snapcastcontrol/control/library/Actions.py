#  Copyright (c) 2021
#
#  This file, Actions.py, is part of Project python-SnapControl.
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


ONMESSAGE               = 'onMessage'


SERVER_GETSTATUS        = 'Server.GetStatus'
SERVER_GETRPCVERSION    = 'Server.GetRPCVersion'
SERVER_DELETECLIENT     = 'Server.DeleteClient'
SERVER_ONUPDATE         = 'Server.OnUpdate'

CLIENT_GETSTATUS        = 'Client.GetStatus'
CLIENT_SETNAME          = 'Client.SetName'
CLIENT_SETLATENCY       = 'Client.SetLatency'
CLIENT_SETSTREAM        = 'Client.SetStream'
CLIENT_SETVOLUME        = 'Client.SetVolume'
CLIENT_ONCONNECT        = 'Client.OnConnect'
CLIENT_ONDISCONNECT     = 'Client.OnDisconnect'
CLIENT_ONVOLUMECHANGED  = 'Client.OnVolumeChanged'
CLIENT_ONLATENCYCHANGED = 'Client.OnLatencyChanged'
CLIENT_ONNAMECHANGED    = 'Client.OnNameChanged'

GROUP_GETSTATUS         = 'Group.GetStatus'
GROUP_SETMUTE           = 'Group.SetMute'
GROUP_SETSTREAM         = 'Group.SetStream'
GROUP_SETCLIENTS        = 'Group.SetClients'
GROUP_ONMUTE            = 'Group.OnMute'
GROUP_ONSTREAMCHANGED   = 'Group.OnStreamChanged'

STREAM_SETMETA          = 'Stream.SetMeta'
STREAM_ONUPDATE         = 'Stream.OnUpdate'
STREAM_ONMETA           = 'Stream.OnMetadata'

SERVER_RECONNECTION_DELAY = 5

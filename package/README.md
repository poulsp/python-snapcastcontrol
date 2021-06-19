# SnapcastControl
> SnapcastControl is a Python API for controlling snapcast over tcp 1705, [snapcast](https://github.com/badaix/snapcast) is a multi-room synchronous audio solution made by baiax.


## Installation

```sh
pip install snapcastcontrol
```

## Usage


```python
>>>

>>> import asyncio
>>> from SnapcastControl.control import SnapcastControl

>>># Simulation notification callback methods.
def testOnVolumeChange(data):
  percent = data['params'].get('volume').get('percent')
  muted   = data['params'].get('volume').get('muted')
  print(f"### This is a callback from SnapcastControl - Simulation onVolumeChange. - percent: {percent}, muted: {muted}")

def testOnClientConnect(data):
  client = data
  print(f"### This is a callback from SnapcastControl - Simulation of onClientConnect. - connected: {client.connected} ")


def testOnClientDisconnect(data):
  print(f"### This is a callback from SnapcastControl - Simulation of onClientDisconnect. - clientId: {data}")


def testOnServerUpdate(data):
  print(f"### This is a callback from SnapcastControl - Simulation of onServerUpdate. - Create a new server dissmis the Old.") # \n serverData: {serverData} ")

def testOnServerCreated(data):
  print(f"### This is a callback from SnapcastControl - Simulation of onServerCreated. - New Server Created ")


def testOnGroupMute(data):
  pass
def testOnServerDisconnect(data):
  pass


>>> Examples notificationCallbacks
testNotificationCallbacks = {
  'onVolumeChange':         testOnVolumeChange,
  'onServerDisconnect':     testOnServerDisconnect,
  'onGroupMute':            testOnGroupMute,
  'onClientConnect':        testOnClientConnect,
  'onClientDisconnect':     testOnServerDisconnect,
  'onServerUpdate':         testOnServerUpdate,
  'onServerCreated':        testOnServerCreated,



}

>>> Available notificationCallbacks.
  'onVolumeChange':
  'onLatencyChanged':
  'onServerDisconnect':
  'onGroupMute':
  'onClientConnect':
  'onClientDisconnect':
  'onServerUpdate':
  'onClientNameChanged':
  'onGroupStreamchanged':
  'onStreamUpdate':
  'onServerCreated':


>>> snapcastControl = SnapcastControl(1, "ThreadSnapcastControl", 'localhost', port=1705, reconnect=True, notificationCallbacks=testNotificationCallbacks)

>>> Her we use a time sleep, the snapcastControl must first start and initialize.
    time.sleep(0.1)

>>> asyncio.run_coroutine_threadsafe(snapcastControl.setVolumeAllClients(55, False), snapcastControl._loop)
>>> Other methods you can call threadsafe, for now
  async def setVolume(clientId, percent, mute):
  async def setVolumeAllClients(percent, mute):
  async def setClientLatency(clientId, latency):
```



## 📜 License. [GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
Ships under GPLv3, it means you are free to use and redistribute the code but are not allowed to use any part of it under a closed license.


## Disclaimer.
This is work in progress and the code is as it is.
Use it at your own risk/fun.



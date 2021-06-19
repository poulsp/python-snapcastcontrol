#!./venv/bin/python

import signal
import asyncio
import time

from snapcastcontrol.control.SnapControl import SnapControl

#-----------------------------------------------
class ConfigurationError(Exception):
  pass

#-----------------------------------------------
class ProgramKilled(Exception):
  pass


#-----------------------------------------------
def signalHandler(signum, frame):
  raise ProgramKilled


#-----------------------------------------------
signal.signal(signal.SIGTERM, signalHandler)
signal.signal(signal.SIGINT, signalHandler)


#-----------------------------------------------
if __name__ == "__main__":

  clients = dict()


  #-----------------------------------------------
  def runAsyncMethod(function, *args, **kwargs):
    print(f'##### runAsyncMethod("{function}", {args}, {kwargs}')
    return asyncio.run_coroutine_threadsafe(function(*args, **kwargs), snapControl._loop)


  #-----------------------------------------------
  # Simulation of MediaVolume onSnapVolumeChange
  def testOnVolumeChange(data):
    percent = data['params'].get('volume').get('percent')
    muted   = data['params'].get('volume').get('muted')
    client  = data['params'].get('id')
    print(f"### This is a callback from SnapControl - Simulation of onVolumeChange. - percent: {percent}, muted: {muted} - client: {client}")

  # Simulation  methods.
  def testOnServerDisconnect(data):
    print(f"### This is a callback from SnapControl - Simulation of onServerDisconnect.  ")

  def testOnGroupMute(data):
    print(f"### This is a callback from SnapControl - Simulation of onGroupMute. - muted: {data}  ")

  def testOnClientConnect(data):
    client = data
    print(f"### This is a callback from SnapControl - Simulation of onClientConnect. - connected: {client.connected} ")


  def testOnClientDisconnect(data):
    client = data
    print(f"### This is a callback from SnapControl - Simulation of onClientDisconnect. - connected: {client.connected} ")


  def testOnServerUpdate(serverData):
    print(f"### This is a callback from SnapControl - Simulation of onServerUpdate. - Create a new server dissmis the Old.") # \n serverData: {serverData} ")

    #serverData: {'groups': [{'clients': [{'config': {'instance': 1, 'latency': 0, 'name': '', 'volume': {'muted': False, 'percent': 95}}, 'connected': True, 'host': {'arch': 'x86_64', 'ip': '127.0.0.1', 'mac': 'xx:xx:xx:xx:xx:xx', 'name': 'pc16', 'os': 'Ubuntu 20.04.2 LTS'}, 'id': 'xx:xx:xx:xx:xx:xx', 'lastSeen': {'sec': 1623081403, 'usec': 723523}, 'snapclient': {'name': 'Snapclient', 'protocolVersion': 2, 'version': '0.25.0'}}, {'config': {'instance': 1, 'latency': 0, 'name': '', 'volume': {'muted': False, 'percent': 95}}, 'connected': True, 'host': {'arch': 'armv6l', 'ip': '192.168.3.70', 'mac': 'yy:yy:yy:yy:yy:yy', 'name': 'satP70', 'os': 'Raspbian GNU/Linux 10 (buster)'}, 'id': 'yy:yy:yy:yy:yy:yy', 'lastSeen': {'sec': 1623081403, 'usec': 886207}, 'snapclient': {'name': 'Snapclient', 'protocolVersion': 2, 'version': '0.24.0'}}], 'id': '02d90930-92c2-d8f5-221c-a7b7183dffef', 'muted': False, 'name': '', 'stream_id': 'default'}], 'server': {'host': {'arch': 'x86_64', 'ip': '', 'mac': '', 'name': 'pc16', 'os': 'Ubuntu 20.04.2 LTS'}, 'snapserver': {'controlProtocolVersion': 1, 'name': 'Snapserver', 'protocolVersion': 1, 'version': '0.25.0'}}, 'streams': [{'id': 'default', 'meta': {'STREAM': 'default'}, 'status': 'playing', 'uri': {'fragment': '', 'host': '', 'path': '/dev/shm/snapfifo', 'query': {'chunk_ms': '20', 'codec': 'flac', 'name': 'default', 'sampleformat': '48000:16:2'}, 'raw': 'pipe:////dev/shm/snapfifo?chunk_ms=20&codec=flac&name=default&sampleformat=48000:16:2', 'scheme': 'pipe'}}]}

  def testOnLatencyChanged(data):
    pass
    print(f"### This is a callback from SnapControl - Simulation of MediaVolume onLatencyChanged. - data: {data} ")

  def testOnServerCreated(data):
    print(f"### This is a callback from SnapControl - Simulation of onServerCreated. - New Server Created ")


  # Simulation of MediaVolume onSnapX method.
  def testOnSomething(data):
    pass
    print(f"### This is a callback from SnapControl - Simulation of onSomething.  ")



  #-----------------------------------------------
  try:
    multiRoomMediaNotificationCallbacks = {
      'onVolumeChange':         testOnVolumeChange,
      'onLatencyChanged':       testOnLatencyChanged,
      'onServerDisconnect':     testOnServerDisconnect,
      'onGroupMute':            testOnGroupMute,
      'onClientConnect':        testOnClientConnect,
      'onClientDisconnect':     testOnClientDisconnect,
      'onServerUpdate':         testOnServerUpdate,
      'onClientNameChanged':    testOnSomething,
      'onGroupStreamchanged':   testOnSomething,
      'onStreamUpdate':         testOnSomething,
      'onServerCreated':        testOnServerCreated,
    }


    snapControl = SnapControl(1, "ThreadSnapControl", 'localhost', reconnect=True, notificationCallbacks=multiRoomMediaNotificationCallbacks)
    time.sleep(0.1)
    asyncio.run_coroutine_threadsafe(snapControl.setVolumeAllClients(60, False), snapControl._loop)

    # time.sleep(2)
    # # print("### Mute")
    # # asyncio.run_coroutine_threadsafe(snapControl.muteGroup('34cd7f65-3662-3368-b49a-8b62d694fed2', True), snapControl._loop)
    # print("### setVolume for 'b4:2e:99:ec:75:05' to 10")
    # asyncio.run_coroutine_threadsafe(snapControl.setVolume("b4:2e:99:ec:75:05", 10, False), snapControl._loop)


    time.sleep(1)
    # print("### UnMute")
    # asyncio.run_coroutine_threadsafe(snapControl.muteGroup('34cd7f65-3662-3368-b49a-8b62d694fed2', False), snapControl._loop)
    print("### setVolume for 'b4:2e:99:ec:75:05' to 50")
    asyncio.run_coroutine_threadsafe(snapControl.setVolume("b4:2e:99:ec:75:05", 50, False), snapControl._loop)

    # time.sleep(2)
    # asyncio.run_coroutine_threadsafe(snapControl.setClientLatency("b4:2e:99:ec:75:05", -1), snapControl._loop)

    while True:
      time.sleep(0.1)

  except ProgramKilled:
    snapControl.closeConnection()
    print("Program killed: running cleanup code")
    print("####################################\n")


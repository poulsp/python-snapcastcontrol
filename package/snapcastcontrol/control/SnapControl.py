#  Copyright (c) 2021
#
#  This file, SnapControl.py, is part of Project python-SnapControl.
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
import random
import threading

# SERVER_GETRPCVERSION,
# SERVER_DELETECLIENT,
# CLIENT_GETSTATUS,
# CLIENT_SETNAME,
# CLIENT_SETSTREAM,
# GROUP_GETSTATUS,
# GROUP_SETSTREAM,
# GROUP_SETCLIENTS,
# STREAM_SETMETA,
# STREAM_ONMETA,

from .library.Actions import (
	ONMESSAGE,
	SERVER_GETSTATUS,
	SERVER_ONUPDATE,
	CLIENT_ONCONNECT,
	CLIENT_ONDISCONNECT,
	CLIENT_SETVOLUME,
	CLIENT_ONVOLUMECHANGED,
	CLIENT_SETLATENCY,
	CLIENT_ONLATENCYCHANGED,
	CLIENT_ONNAMECHANGED,
	GROUP_SETMUTE,
	GROUP_ONMUTE,
	GROUP_ONSTREAMCHANGED,
	STREAM_ONUPDATE,
	SERVER_RECONNECTION_DELAY
)

from .library.SnapControlProtocol  import (SnapControlProtocol, SERVER_ONDISCONNECT)
from .library.Server import (Server)


#class Host():
#-----------------------------------------------
#class Client():
#-----------------------------------------------
#class Group():
#-----------------------------------------------
#class Stream():
#-----------------------------------------------
#class Server():


#-----------------------------------------------
class SnapControl(threading.Thread):
	def __init__(self, threadID, name, host, port=1705, reconnect=True, notificationCallbacks={}):
		super(SnapControl, self).__init__()

		self.threadID = threadID
		self._name = name

		self._notificationCallbacks = notificationCallbacks
		self._host = host
		self._port = port
		self._reconnect = reconnect
		self._statusReqId = -1
		self.data = None
		self.server = None
		self._protocol = None
		self._loop = ""

		self._callbacks = {
			ONMESSAGE: self._onMessage,
			SERVER_ONDISCONNECT: self._onServerDisconnect,
		}

		self.daemon = True
		self.start()

	@property
	def loop(self):
		return self._loop


	#-----------------------------------------------
	def _onServerDisconnect(self, exception):
		print(f"##### Go into _onServerDisconnect")
		# Close the socket.
		self.transport.close()
		self._protocol = None
		self._statusReqId = -1
		# Alert/notify caller.
		if self._notificationCallbacks.get('onServerDisconnect'):
			self._notificationCallbacks.get('onServerDisconnect')(exception)

		if self._reconnect:
			self._reconnecting()


	#-----------------------------------------------
	def _reconnecting(self):
		async def attempt2Reconnect():
			try:
				await self._connect()

			except IOError:
				# An instance of asyncio.TimerHandle is returned which can be used to cancel the callback.
				self._loop.call_later(SERVER_RECONNECTION_DELAY, self._reconnecting)

		asyncio.create_task(attempt2Reconnect())


	#-----------------------------------------------
	# Thread run
	def run(self):
		# Start the SnapControl and the Event loop.
		self._loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self._loop)
		try:

			self._loop.create_task(self._asyncStart())
			self._loop.run_forever()
		except Exception as e:
				print(f"Thread run Exception e: {e}")
				raise e


	#-----------------------------------------------
	async def _asyncStart(self):
		# print("Go Into start")
		await self._connect()
		await self.setVolumeAllClients(30, False)


	#-----------------------------------------------
	def closeConnection(self):
		# print("Go into closeConnection")
		# Close the socket.
		self.transport.close()
		self._protocol = None
		self._loop.stop()


	#-----------------------------------------------
	async def _connect(self):
		# print(f"#### Go into _connect")
		try:

			self.transport, self._protocol = await self._loop.create_connection(
				lambda: SnapControlProtocol(self._callbacks), self._host, self._port)

			response = await self._sendReq(SERVER_GETSTATUS)
			self._onMessage(response)

			return response

		except Exception as e:
			raise e


		# An identifier established by the Client that MUST contain a String, Number, or NULL value if included.
		# If it is not included it is assumed to be a notification. The value SHOULD normally not be Null [1] and Numbers SHOULD NOT contain fractional parts [2]


	#-----------------------------------------------
	def _action(self, answer):
		value = answer['method']

		if value == CLIENT_ONVOLUMECHANGED:
			# Alert/notify caller.
			if self._notificationCallbacks.get('onVolumeChange'):
				self._notificationCallbacks.get('onVolumeChange')(answer)

			else:
				client = self.getClient(answer['params']['id'])
				client.config['volume'] = answer.get('params').get('volume')

		elif value == CLIENT_ONLATENCYCHANGED:
			client = self.getClient(answer['params']['id'])
			client.latency = answer.get('params').get('latency')

			if self._notificationCallbacks.get('onLatencyChanged'):
				self._notificationCallbacks.get('onLatencyChanged')(answer)

		elif value == CLIENT_ONNAMECHANGED:
			client = self.getClient(answer['params']['id'])
			client.name = answer.get('params').get('name')

			if self._notificationCallbacks.get('onClientNameChanged'):
				self._notificationCallbacks.get('onClientNameChanged')(answer)


		elif value == CLIENT_ONCONNECT or value == CLIENT_ONDISCONNECT:
			method =  answer.get('method')
			clientId =  answer.get('params').get('client').get('id')
			client = self.getClient(clientId)
			client.connected = answer.get('params').get('client').get('connected')

		# Alert/notify caller.
			if method == CLIENT_ONCONNECT:
				if self._notificationCallbacks.get('onClientConnect'):
					# self._notificationCallbacks.get('onClientConnect')(client)
					self._notificationCallbacks.get('onClientConnect')(answer)

			elif method == CLIENT_ONDISCONNECT:
				if self._notificationCallbacks.get('onClientDisconnect'):
					# self._notificationCallbacks.get('onClientDisconnect')(client)
					self._notificationCallbacks.get('onClientDisconnect')(answer)

		elif value == GROUP_ONMUTE: #TODO
			group = self.getGroup(answer['params']['id'])
			group.muted = answer.get('params').get('mute')

			# Alert/notify caller.
			if self._notificationCallbacks.get('onGroupMute'):
				self._notificationCallbacks.get('onGroupMute')(answer.get('params'))

		elif value == GROUP_ONSTREAMCHANGED:
			if self._notificationCallbacks.get('onGroupStreamchanged'):
				self._notificationCallbacks.get('onGroupStreamchanged')(answer)

			# TODO ?
			# print(f"###### in switch -- value: {value}")
			# #print(f"###### in switch -- answer: {answer}")
			# #group = self.getGroup(answer['params'].get('id'))
			# # self.getGroup(answer['params']['id'])['streamId'] = answer.get('params').get('streamId')


		elif value == STREAM_ONUPDATE:
			if self._notificationCallbacks.get('onStreamUpdate'):
				self._notificationCallbacks.get('onStreamUpdate')(answer)

		#   # TODO ?
		#   print(f"###### 4.) in switch -- value: {value}")
		#   print(f"###### in switch -- answer: {answer}")
		#   ## in switch -- answer: {'jsonrpc': '2.0', 'method': 'Stream.OnUpdate', 'params': {'id': 'default', 'stream': {'id': 'default', 'meta': {'STREAM': 'default'}, 'status': 'playing', 'uri': {'fragment': '', 'host': '', 'path': '/dev/shm/snapfifo', 'query': {'chunk_ms': '20', 'codec': 'flac', 'name': 'default', 'sampleformat': '48000:16:2'}, 'raw': 'pipe:////dev/shm/snapfifo?chunk_ms=20&codec=flac&name=default&sampleformat=48000:16:2', 'scheme': 'pipe'}}}}

		# #   # self.getStream(answer['params']['id']) = get('params').get('stream')['id']

		elif value == SERVER_ONUPDATE:
			self._statusReqId = random.randint(1, 1000) #answer['id']

			# Alert/notify caller.
			serverData = answer.get('params').get('server')
			self.server = Server(serverData)

			if self._notificationCallbacks.get('onServerUpdate'):
				self._notificationCallbacks.get('onServerUpdate')(serverData)

		else:
			pass


	#-----------------------------------------------
	def getClient(self, clientId):
		client = self.server.getClient(clientId)

		if not client:
			print(f" raise an Error(`client {clientId} was None`)")

		return client


	#-----------------------------------------------
	def getClients(self):

		clients = self.server.getClients()

		if not clients:
			print(f" raise an ErrorNo clients`)")
		else:
			return clients


	#-----------------------------------------------
	def getGroup(self, group_id):
		pass
		group = self.server.getGroup(group_id);
		if not group:
			print(f" raise an Error(`client {group_id} was None`)")

		return group;


	#-----------------------------------------------
	async def setVolume(self, clientId, percent, mute):
		# print("Going into setVolume")

		percent = max(0, min(100, percent))

		client = self.getClient(clientId);
		client.volumeLevel = percent
		client.muted = mute

		response = await self._sendReq(CLIENT_SETVOLUME, {
			 'id': clientId,
				'volume': {
					'muted': mute, 'percent': percent
				}
		})

		return response


	#-----------------------------------------------
	async def setVolumeAllClients(self, percent, mute):
		# Temporary
		for group in self.server.groups:
			for client in group.clients:
				client.config['volume']['percent'] = percent
				if mute:
					client.config['volume']['muted'] = mute

				await self._sendReq(CLIENT_SETVOLUME, {
					 'id': client.id,
						'volume': {
							'muted': mute, 'percent': percent
						}
				})

	#-----------------------------------------------
	async def setClientLatency(self, clientId, latency):
		client = self.getClient(clientId);

		if latency != client.latency:
			response = await self._sendReq(CLIENT_SETLATENCY, {
										'id': clientId,
										'latency': latency
									}
								)
			client.latency = latency


		return response


# # Future TODO
	#-----------------------------------------------
	# def getGroupVolume(self, group):
	#   pass
	# #-----------------------------------------------
	# def getGroupFromClient(self, clientId):
	#   pass
	# #-----------------------------------------------
	# def getStream(self, streamId):
	#   pass
	# #-----------------------------------------------
	# def setGroupName(self ,group_id, name):
	#   pass
	#   # print(f"In setGroupName - name: {name}")
	# #-----------------------------------------------
	# def setClientName(self,clientId, name):
	#   pass
	# #-----------------------------------------------
	# def deleteClient(self,clientId):
	#   pass
	# #-----------------------------------------------
	# def setStream(self,group_id, streamId):
	#   pass
	# #-----------------------------------------------
	# def setClients(self,group_id, clients):
	#   pass


	#-----------------------------------------------
	async def muteGroup(self, group_id, mute):
		self.getGroup(group_id).muted = mute

		await self._sendReq(GROUP_SETMUTE, {
			 'id': group_id,
				'mute': mute
		})


#-----------------------------------------------
	async def _sendReq(self, method, params=None):
		try:
			result = await self._protocol.request(method, params)
		except IOError as e:
			print(f"_sendReq IOError: {e}")
			raise e
		return result


	#-----------------------------------------------
	def _onMessage(self,msg):
		answer = msg
		# print("Going into OnMessage")

		if 'id' in answer: # response from request
			if self._statusReqId == -1:
				self._statusReqId = answer['id']

			if answer['id'] == self._statusReqId:
				self.server = Server(answer['result']['server'])
				# Alert/notify caller.
				if self._notificationCallbacks.get('onServerCreated'):
					self._notificationCallbacks.get('onServerCreated')(answer['result']['server'])


		else: # a notification.
			if isinstance(answer, list):
				for ans in answer:
					self._action(ans)
			else:
				self._action(answer)

		# print("Going out of OnMessage")

		return answer



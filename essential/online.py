"""
The interface for communicating with the message server
"""

class RedisTransition:
	def __init__(self, server_ip, server_port, channel_name):
		"""
		Constructor

		@param server_ip Specify the ip of the redis server
		@param server_port Specify the port of the redis server
		@param channel_name Specify the name of the channel in the redis server
		       to be communicated.
		"""
		from asgiref.sync import async_to_sync
		from channels_redis.core import RedisChannelLayer

		self._redis_server = RedisChannelLayer(hosts = [(server_ip, int(server_port))])
		self._channel_name = channel_name

	def send(self, message_object):
		async_to_sync(self._redis_server.send)(self._channel_name, message_object)

MessageServer = RedisTransition

class TransitionManager:
	"""
	Receive data sent from the game process and pass it to the remote server
	"""

	def __init__(self, recv_data_func, server_info):
		"""
		Constructor

		@param recv_data_func The function for receiving data
		@param server_info The information of the remote server.
		       A three-element tuple (server_ip, server_port, channel_name).
		"""
		self._recv_data_func = recv_data_func
		self._message_server = MessageServer(*server_info)

	def transition_loop(self):
		"""
		The infinite loop for passing data to the remote server
		"""
		try:
			while True:
				data = self._recv_data_func()
				self._message_server.send(data)
		except Exception as e:
			print(e)

from app import sockeio

def disconnect_old_socketio(func):
	@wraps(func)
	def wrapper(*args,**kargs):
		sockeio.disconnect()     
		return func(*args,**kargs)
	return wrapper
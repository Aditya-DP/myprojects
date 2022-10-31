import pyshark 
import signal,sys
import json
import asyncio, concurrent
import nest_asyncio
nest_asyncio.apply()
capture = pyshark.LiveCapture(interface='eno1', display_filter='udp.port==68')

def exception_handler(sig, frame):
	print('Exit')
	capture.close()
	sys.exit(0)


packet_details={}

def packet_process(pkt):
	list_updated=False
	mac=pkt.bootp.hw_mac_addr
	if mac not in packet_details:
		list_updated=True
		packet_details[mac]='No hostname'
		try:
			packet_details[mac]=pkt.bootp.option_hostname
		except AttributeError:
			pass
	if list_updated:
		print(packet_details)
		list_updated=False


if __name__=="__main__":
	signal.signal(signal.SIGINT, exception_handler)
	try:
		capture.apply_on_packets(packet_process,timeout=20)
	except asyncio.TimeoutError as e:
		print("Timeout reached")

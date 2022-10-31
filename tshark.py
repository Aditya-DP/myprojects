import pyshark 
import sys,os
import json
capture = pyshark.LiveCapture(interface='eno1', display_filter='udp.port==68')

capture.sniff(packet_count=20)
packet_details = {}

for pkt in capture:
	mac = pkt.bootp.hw_mac_addr
	packet_details[mac]= 'No hostname'
	try:
		packet_details[mac]=pkt.bootp.option_hostname
		
	except AttributeError:
		pass
print(json.dumps(packet_details, indent=1))

capture.close()
sys.exit(0)

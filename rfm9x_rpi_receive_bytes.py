# Example to receive addressed packed with ACK
# Author: Jerry Needell
#
import time
import board
import busio
import digitalio
import adafruit_rfm9x

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip.
# set GPIO pins as necessary - this example is for Raspberry Pi
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
# set address to Node 0 - ignore packets to other addresses
rfm9x.node = 0
# enable CRC checking
rfm9x.enable_crc = True
# set delay before transmitting ACK (seconds)
rfm9x.ack_delay = 0.1

# Wait to receive packets.
print("Waiting for packets...")
while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm9x.receive(with_ack=True, with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("RSSI: {0}".format(rfm9x.last_rssi))
        packet_header = packet[0:4]
        packet_payload = packet[4:]
        print("Received (raw header):", [hex(x) for x in packet_header[0:4]])
        print("Received (raw payload):", [hex(x) for x in packet_payload])
        count = packet_payload[0]
        subcount = packet_payload[1]
        error_count = packet_payload[2]
        battery_voltage = (packet_payload[3] + 256*packet_payload[4])/1000.
        battery_charge_level= packet_payload[5] 
        print("{} {} {} {}V {}%".format(count,subcount,error_count,battery_voltage,battery_charge_level))

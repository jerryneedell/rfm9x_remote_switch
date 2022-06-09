import alarm
import time
import board
import digitalio
import adafruit_rfm9x
from adafruit_lc709203f import LC709203F, PackSize

if alarm.wake_alarm:
    #print("awake", alarm.wake_alarm, alarm.wake_alarm.pin)
    print("awake", alarm.wake_alarm)
    alarm.sleep_memory[0] += 1
else:
    print("no wake up alarm")
    alarm.sleep_memory[0] = 0
    alarm.sleep_memory[2] = 0

sensor = LC709203F(board.I2C())
sensor.pack_size = PackSize.MAH1000 


#turn on the LED while it is awake
led=digitalio.DigitalInOut(board.LED)
led.switch_to_output()
led.value = True

# this is the alarm pin
pin=digitalio.DigitalInOut(board.A4)
pin.pull  = digitalio.Pull.UP

print("count:", alarm.sleep_memory[0])

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip.
CS = digitalio.DigitalInOut(board.D10)
RESET = digitalio.DigitalInOut(board.D11)

# Initialize SPI bus.
#spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi = board.SPI()

# Initialze RFM radio
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.node = 1
rfm9x.destination = 0
rfm9x.tx_power = 23


# send a mesage as long as the pin is low
alarm.sleep_memory[1] = 0

byte_packet = bytearray(10)
while not pin.value:
    voltage = int(sensor.cell_voltage*1000)
    cell_level = int(sensor.cell_percent)
    byte_packet[0] = alarm.sleep_memory[0]
    byte_packet[1] = alarm.sleep_memory[1]
    byte_packet[2] = alarm.sleep_memory[2]
    byte_packet[3] = voltage&0xff
    byte_packet[4] = (voltage>>8)&0xff
    byte_packet[5] = cell_level&0xff

    if not rfm9x.send_with_ack(bytes(byte_packet)):
        alarm.sleep_memory[2] += 1
        print("No Ack")
    time.sleep(3.)
    alarm.sleep_memory[1] += 1

#free the alarm pin
pin.deinit()

rfm9x.sleep()
print("packet sent - rfm9x sleeping")

#create an alarm on Pin IO5
pin_alarm = alarm.pin.PinAlarm(pin=board.A4, value=False, pull=True)


print("about to deep_sleep")

# exit and set the alarm
alarm.exit_and_deep_sleep_until_alarms(pin_alarm)


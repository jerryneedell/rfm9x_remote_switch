# rfm9x_remote_switch
send switch status via LoRa

There are two versions of the transmit and receive programs. The first (alarm_rfm9x_ack.py and rfmnx_rpi_receive.py) sends an Ascii string with some words and data. The second (alarm_rfm9x_ack_bytes.py and rfm9x_rpi_receive_bytes.py) sends a byte array containing the data vaules. I like the second method because the packets are much smaller and it is much easier to decode the data on the receiving side wthout having to parse the Ascii string.


**files:**

* alarm_rfm9x_ack.py  -- for Adafruit feather esp32s2 - sends switch status in ascii
* alarm_rfm9x_ack_bytes.py  -- for Adafruit feather esp32s2 - sends switch status as bytes not ascii
* alarm_rfm9x_ack_pack.py  -- for Adafruit feather esp32s2 - sends switch status as packed struct
* rfm9x_rpi_receive.py  -- for Raspberry Pi - receives switch status sends Ack
* rfm9x_rpi_receive_bytes.py  -- for Raspberry Pi - receives switch status as bytes sends Ack
* rfm9x_rpi_receive_pack.py  -- for Raspberry Pi - receives switch status as packed struct sends Ack
* rfm9x_rpi_header.py  -- receives aand prints any LoRa packets
* rfm9x_rpi_ack.py  --  receives, prints and acknowledges any Lora packet


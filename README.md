# rfm9x_remote_switch
send switch status via LoRa


files:
alarm_rfm9x_ack.py  -- for Adafruit feather esp32s2 - sends switch status
rfm9x_rpi_receive.py  -- for Raspberry Pi - receives switch status sends Ack
rfm9x_rpi_header.py  -- receives aand prints any LoRa packets
rfm9x_rpi_ack.py  --  receives, prints and acknowledges any Lora packet

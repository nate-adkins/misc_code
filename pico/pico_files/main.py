import select, sys, time, machine

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

led = machine.Pin(25, machine.Pin.OUT)


temp_sensor = machine.ADC(4)
def read_temperature():
    adc_value = temp_sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 2)

# Loop indefinitely
while True:
    # Wait for input on stdin
    poll_results = poll_obj.poll(5) # the '1' is how long it will wait for message before looping again (in microseconds)
    if poll_results:

        temp = read_temperature()
        data = sys.stdin.readline().strip()
        data = 4 * int(data)
        sys.stdout.write("four times the input: " + str(data) + " Temp: " + str(temp) + "\r")
        led.value(not led.value()) 
    else:
        # do something if no message received (like feed a watchdog timer)
        continue
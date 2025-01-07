import RPi.GPIO as GPIO
from time import sleep
from Hardware import DHT22 as dht
from Hardware import usonic as us
from Hardware import adc as adc
from Hardware import Buzzer as buz
from Hardware import lcd as lcd
from Hardware import Switch as sw
from Hardware import Keypad as keypad
from threading import Thread
import thingspeak as upload
import button_3
import button_4  # Uncomment if used
import button_5
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import csv
from datetime import datetime

# Initialize hardware modules
lcd=lcd.lcd()
sleep(0.5)
lcd.lcd_clear()
sleep(0.5)
us.init()
dht.init()
adc.init()
buz.init()
sw.init()

# Global variable for device state
ON_OFF_DEVICE = 1
run = True

# Keypad configuration
ROW = [6, 20, 19, 13]  # GPIO pins for rows
COL = [12, 5, 16]      # GPIO pins for columns
MATRIX = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ['*', 0, '#']
]  # Keypad layout

def init_keypad(key_press_cbk):
    """Initialize the keypad with the callback function."""
    global cbk_func
    cbk_func = key_press_cbk

    # Set column pins as outputs and write default value of 1 to each
    for col in COL:
        GPIO.setup(col, GPIO.OUT)
        GPIO.output(col, 1)

    # Set row pins as inputs with pull-up resistors
    for row in ROW:
        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def get_key():
    """Continuously scan the keypad."""
    global cbk_func
    while True:
        for col_index, col in enumerate(COL):  # Loop through all columns
            GPIO.output(col, 0)  # Pull one column pin low
            for row_index, row in enumerate(ROW):  # Check which row pin becomes low
                if GPIO.input(row) == 0:  # Key press detected
                    cbk_func(MATRIX[row_index][col_index])  # Call the callback function
                    while GPIO.input(row) == 0:  # Debounce
                        sleep(0.1)
            GPIO.output(col, 1)  # Restore default value of 1

def record_time():
    """Record the current time and date."""
    current_time = datetime.now().strftime("%X")
    current_date = datetime.now().strftime("%x")
    print(current_time)
    print(current_date)
    return current_time, current_date

def record_location(phone_number):
    """Record the location based on the phone number using OpenCage Geocode."""
    try:
        parsed_number = phonenumbers.parse(phone_number)
        number_location = geocoder.description_for_number(parsed_number, "en")
        key = 'c1f1ab0aed724b25aef695ed8b4de102'
        oc_geocoder = OpenCageGeocode(key)
        query = str(number_location)
        results = oc_geocoder.geocode(query)
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        print(lat, lng)
        #global variable
        global latti, long
        latti=lat
        long=lng
        #end
        return int(lat), int(lng)
    except Exception as e:
        print(f"Error recording location: {e}")
        return None, None

def record_humi_and_temp():
    """Record the temperature and humidity from the DHT22 sensor."""
    temperature, humidity = dht.read_temp_humidity()
    if temperature != -100 or humidity != -100:
        print(int(temperature), int(humidity))
        global tempe,humi
        tempe=temperature
        humi=humidity
        return int(temperature), int(humidity)
    else:
        print(30, 60)
        return 30, 60

def record_ldr():
    """Record the light intensity from the ADC."""
    try:
        intensity = adc.get_adc_value(0)
        print(int(intensity))
        global intense
        intense=intensity
        return int(intensity)
    except Exception as e:
        print(f"Error recording light intensity: {e}")
        return None

def record_ultrasonic():
    """Record the distance from the ultrasonic sensor."""
    try:
        distance = us.get_distance()
        sleep(1)
        print(int(distance))
        return int(distance)
    except Exception as e:
        print(f"Error recording distance: {e}")
        return None

def key_pressed(key):
    """Handle key press events."""
    global ON_OFF_DEVICE, run
    if key == 1:
        run = False
        button_3.main()
        run = True
    elif key== 2:
        run = False
        button_4.main("i am lost")
        run = True
    elif key == 3:
        run = False
        button_5.main()
        run = True

def track():
    """Track and record data continuously while the device is on."""
    init_keypad(key_pressed)  # Initialize the keypad with the callback function

    keypad_thread = Thread(target=get_key)
    keypad_thread.daemon = True  # Ensure the thread exits when the main program does
    keypad_thread.start()
    # Open CSV file for appending data, create headers if the file is empty
    with open('track.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if csvfile.tell() == 0:
            csvwriter.writerow(['Time', 'Date', 'Latitude', 'Longitude', 'Temperature', 'Humidity', 'Intensity', 'Distance'])
    
    while True:
        global ON_OFF_DEVICE
        ON_OFF_DEVICE = sw.read()
        if ON_OFF_DEVICE == 1 and run:
            print("ON")
            # Clear and display initial tracking message on LCD
            lcd.lcd_clear()
            lcd.lcd_display_string("start_tracking")
            sleep(2)
            lcd.lcd_clear()

            # Continuously record data
            while ON_OFF_DEVICE == 1:
                try:
                    upload.send_data(temperature, humidity, intensity, latitude, longitude)
                except UnboundLocalError:
                    print('First Upload Skipped')
                current_time, current_date = record_time()
                latitude, longitude = record_location("+65 88564133")  # Provide the phone number
                intensity = record_ldr()
                temperature, humidity = record_humi_and_temp()
                sleep(2)

                if temperature < 20 or humidity > 80 or intensity < 350:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Going to rain")
                    buz.beep(2, 1, 1)
                    lcd.lcd_clear()
                else:
                    lcd.lcd_display_string("Sunny")

                distance = record_ultrasonic()

                if distance < 30:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("obstical")
                    buz.beep(1, 1, 5)
                    lcd.lcd_clear()

                with open('track.csv', 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([current_time, current_date, latitude, longitude, temperature, humidity, intensity, distance])
                print('Looping')

                ON_OFF_DEVICE = sw.read()
        else:
            print("OFF")

if __name__ == '__main__':
    track()

def background_task():
    while True:
        """
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(Tsampling/1000000)
        outVo = adc.read_adc(dustPin, gain=GAIN)*(5.0/7081.0);
        time.sleep(Tdelta/1000000)
        GPIO.output(ledPin, GPIO.HIGH)
        time.sleep(Tsleep/1000000)
        dustLevel = (0.17 * outVo - 0.1)*1000.0;
        if (dustLevel< 0):
            dustLevel = 0.00;
        # Read all the ADC channel values in a list.
        Smoke_val = 0
        CO_val = 0
        # Defining constants
        r0 = 76.63
        ppm = .0
        RL = 10.0
        # The read_adc function will get the value of the specified channel (0-7).
        Smoke_val = adc.read_adc(1, gain=GAIN)
        CO_val = adc.read_adc(0, gain=GAIN)
        # Calculating Smoke and CO values
        #Smoke_sensor_volt = Smoke_val*(5.0/24470.0)
        CO_sensor_volt = CO_val*(5.0/29870.0)
        RS_Smoke = ((1023.0/Smoke_val*5.0-1.0)*RL)/0.52295515
        #RS_Smoke =(5.0*RL-(RL*Smoke_sensor_volt))/Smoke_sensor_volt
        CO_ratio = (5.0-CO_sensor_volt)/CO_sensor_volt
        #CO2_ppm = (146.15*(2.868-RS_Smoke/r0* 0.3611)+10.0)
        CO2_ppm = 116.6020682*pow(RS_Smoke/r0, -2.769034857)
        CO_ppm = 19.32*pow(CO_ratio,-0.64)
        #ppm = 47.947*CO_sensor_volt - 79.73501
        temperature =  sensor.temperature
        humidity = sensor.relative_humidity
        print("\nTemperature: {:0.1f} C".format(temperature))
        print("Humidity: {:.1f}".format(humidity))
        # Print the ADC values.
        print("Dust Density Level (in ug/m^3): {:.5f}".format(dustLevel));
        print('CO ppm: {:.2f}'.format(CO_ppm))
        print('Smoke(CO2) ppm: {:.2f}'.format(CO2_ppm))
        """
        temperature = 2.0
        #display_text(f"CO: %0.1f" % CO_ppm, f"CO2: %0.1f" % CO2_ppm , f"Dust: %0.1f" % dustLevel)
        time.sleep(0.5)
        #display_text(f"Temp: %0.1f C" % temperature, f"Humi: %0.1f %%" % humidity, f"")
        time.sleep(0.5)  # You can adjust the sampling interval
        pass
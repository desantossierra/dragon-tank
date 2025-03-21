import RPi.GPIO as GPIO
import time

class Sonar:
    """Clase para controlar el sensor ultrasónico."""

    def __init__(self, trigger_pin, echo_pin):
        """Inicializa el sensor con los pines GPIO."""
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.setup()

    def setup(self):
        """Configura los pines GPIO para el sensor."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def distance(self):
        """Lee la distancia medida por el sensor."""
        for _ in range(5):  # Remove invalid test results.
            GPIO.output(self.trigger_pin, GPIO.LOW)
            time.sleep(0.000002)
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.000015)
            GPIO.output(self.trigger_pin, GPIO.LOW)

            while not GPIO.input(self.echo_pin):
                pass
            t1 = time.time()
            while GPIO.input(self.echo_pin):
                pass
            t2 = time.time()
            dist = (t2 - t1) * 340 / 2

            if dist > 9 and _ < 4:  # 5 consecutive times are invalid data, return the last test data
                continue
            else:
                return dist * 100  # Convert to centimeters

    def cleanup(self):
        """Limpia los pines GPIO."""
        GPIO.cleanup((self.trigger_pin, self.echo_pin))

# Pines GPIO para el sensor ultrasónico
TRIGGER_PIN = 11
ECHO_PIN = 8

if __name__ == '__main__':
    try:
        sonar = Sonar(TRIGGER_PIN, ECHO_PIN)
        while True:
            distance = sonar.distance()
            print("%.2f cm" % distance)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        if 'sonar' in locals():
            sonar.cleanup()
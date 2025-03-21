import RPi.GPIO as GPIO
import time

class Wheel:
    """Clase para controlar una rueda."""

    def __init__(self, enable_pin, pin1, pin2):
        """Inicializa la rueda con los pines GPIO."""
        self.enable_pin = enable_pin
        self.pin1 = pin1
        self.pin2 = pin2
        self.pwm = None

    def setup(self):
        """Configura los pines GPIO para la rueda."""
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        self.stop()  # Inicializa la rueda en estado de parada
        try:
            self.pwm = GPIO.PWM(self.enable_pin, 1000)
        except Exception as e:
            print(f"Error al configurar PWM para la rueda {self.enable_pin}: {e}")

    def forward(self, speed):
        """Mueve la rueda hacia adelante."""
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)
        if self.pwm:
            self.pwm.start(100)
            self.pwm.ChangeDutyCycle(speed)

    def backward(self, speed):
        """Mueve la rueda hacia atrás."""
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.HIGH)
        if self.pwm:
            self.pwm.start(100)
            self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        """Detiene la rueda."""
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)
        GPIO.output(self.enable_pin, GPIO.LOW)

    def cleanup(self):
        """Detiene la rueda y limpia los pines GPIO."""
        self.stop()
        if self.pwm:
            self.pwm.stop()


MOTOR_A_EN = 4
MOTOR_A_PIN1 = 15
MOTOR_A_PIN2 = 14
MOTOR_B_EN = 17
MOTOR_B_PIN1 = 27
MOTOR_B_PIN2 = 18

class Wheels:
    """Clase para controlar ambas ruedas del robot."""

    def __init__(self):
        """Inicializa las ruedas con instancias de la clase Wheel."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Crea instancias de las ruedas
        self.left_wheel = Wheel(MOTOR_B_EN, MOTOR_B_PIN1, MOTOR_B_PIN2)
        self.right_wheel = Wheel(MOTOR_A_EN, MOTOR_A_PIN1, MOTOR_A_PIN2)

    def setup(self):
        """Configura ambas ruedas."""
        self.left_wheel.setup()
        self.right_wheel.setup()

    def forward(self, speed):
        """Mueve el robot hacia adelante."""
        self.left_wheel.forward(speed)
        self.right_wheel.forward(speed)

    def backward(self, speed):
        """Mueve el robot hacia atrás."""
        self.left_wheel.backward(speed)
        self.right_wheel.backward(speed)

    def turn_left(self, speed, radius=0.6):
        """Gira el robot a la izquierda."""
        self.right_wheel.forward(speed)
        self.left_wheel.backward(int(speed * radius))

    def turn_right(self, speed, radius=0.6):
        """Gira el robot a la derecha."""
        self.right_wheel.backward(int(speed * radius))
        self.left_wheel.forward(speed)

    def stop(self):
        """Detiene ambas ruedas."""
        self.left_wheel.stop()
        self.right_wheel.stop()

    def cleanup(self):
        """Detiene las ruedas y limpia los pines GPIO."""
        self.left_wheel.cleanup()
        self.right_wheel.cleanup()

if __name__ == "__main__":
    try:
        wheels = Wheels()
        wheels.setup()

        # Mueve el robot hacia adelante
        wheels.forward(80)
        time.sleep(2)

        # Gira el robot a la izquierda
        wheels.turn_left(60, radius=1)
        time.sleep(2)

        # Mueve el robot hacia atrás
        wheels.backward(70)
        time.sleep(2)

        # Gira el robot a la derecha
        wheels.turn_right(60, radius=1)
        time.sleep(2)

        # Detiene el robot
        wheels.stop()
        time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted by user")


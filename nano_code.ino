#include <TimerOne.h>

// CONFIGURARE PINI
const int BACKLIGHT_PIN = 9; 

// VARIABILE CONTROL
double uk, yk, yk_1;
double C, T_proces;
float Refk = 500.0; 
float Te = 0.1;     // Perioada esantionare
float data3 = 0, data4 = 0;

// VARIABILE PWM DIMMING
float smoothed_val = 128;
int pwm_val = 128;

void setup() {
  pinMode(BACKLIGHT_PIN, OUTPUT);
  
  // CONFIGURARE ADC
  ADMUX = (1 << REFS0);
  ADCSRA = (1 << ADEN) | (1 << ADSC) | (1 << ADATE) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); 

  // Initializare variabile
  uk = 0; yk = 0; yk_1 = 0;
  T_proces = 10; 
  C = Te / (Te + T_proces);      
  
  // Initializare Timer cu perioada Te
  Timer1.initialize((long)(Te * 1000000));
  Timer1.attachInterrupt(esantionare);
}

void loop() {
  //gol
}

// esantionare (ISR)
void esantionare() {
  // ESANTIONARE ADC
  int raw = ADC; 
  
  // LOGICA PWM
  smoothed_val = (0.05 * raw) + (0.95 * smoothed_val);
  pwm_val = map((int)smoothed_val, 50, 400, 50, 255);
  pwm_val = constrain(pwm_val, 50, 255);
  analogWrite(BACKLIGHT_PIN, pwm_val);

  // ALGORITM DE CONTROL
  uk = Refk;
  yk = yk_1 + C * (uk - yk_1);
  yk_1 = yk;
}

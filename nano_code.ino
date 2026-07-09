// Parametrii de filtrare si control
volatile unsigned long senzor_filtrat = 0;  
volatile uint8_t pwm_target = 15; 

// Parametrii de Autocalibrare
volatile unsigned long counter_esantioane = 0;
volatile unsigned long senzor_max_calibrat = 50; 
volatile unsigned long divizor_gamma = 10924481UL; 
volatile bool calibrare_gata = false;

// Masca pentru pinii D3, D4 si D5
const uint8_t MASCA_PINI = (1 << DDD3) | (1 << DDD4) | (1 << DDD5);

void setup() {
  // 1. CONFIGURARE D3, D4, D5 (Iesire nativa pe LOW/GND in paralel)
  PORTD &= ~MASCA_PINI; 
  DDRD &= ~MASCA_PINI;  

  // 2. CONFIGURARE TIMER 1 (Open-Drain pe 3 Pini)
  TCCR1A = (1 << WGM10);  
  TCCR1B = (1 << WGM12) | (1 << CS12); 
  OCR1A = 15; 
  TIMSK1 = (1 << TOIE1) | (1 << OCIE1A);

  // 3. CONFIGURARE ADC (Senzor pe A0)
  ADMUX = (1 << REFS0); 
  ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

  // 4. CONFIGURARE TIMER 2 (Esantionare la 10ms)
  TCCR2A = (1 << WGM21);
  TCCR2B = (1 << CS22) | (1 << CS21) | (1 << CS20);
  OCR2A = 155; 
  TIMSK2 = (1 << OCIE2A);
  senzor_filtrat = analogRead(A0);
  // 5. PASTRAM SERIALUL PENTRU DEBUGGING
  Serial.begin(9600); 
}

void loop() {
  // BLOCUL DE SUPERVIZARE / AUTOCALIBRARE
  if (!calibrare_gata && counter_esantioane >= 500) {
    if (senzor_max_calibrat < 20) senzor_max_calibrat = 20; 
    
    // Curba Patratica
    unsigned long patrat_maxim = senzor_max_calibrat * senzor_max_calibrat;
    divizor_gamma = patrat_maxim / 95UL;
    
    if (divizor_gamma == 0) divizor_gamma = 1;
    calibrare_gata = true; 
    
    Serial.println("========================================");
    Serial.print("AUTOCALIBRARE GATA! Max camera: ");
    Serial.println(senzor_max_calibrat);
    Serial.print("Divizor Patratic calculat: ");
    Serial.println(divizor_gamma);
    Serial.println("========================================");
  }
  
  // Monitorizare in timp real pe Serial
  if (calibrare_gata) {
    Serial.print("Senzor Filtrat: ");
    Serial.print(senzor_filtrat);
    Serial.print(" | PWM Trimis (OCR1A): ");
    Serial.println(OCR1A);
  } else {
    Serial.print("[CALIBRARE] Esantion: ");
    Serial.print(counter_esantioane);
    Serial.print("/500 | Max Curent: ");
    Serial.println(senzor_max_calibrat);
  }
  
  delay(100); 
}

// ISR Timer 2
ISR(TIMER2_COMPA_vect) {
  ADCSRA |= (1 << ADSC); 
}

// ISR ADC
ISR(ADC_vect) {
  unsigned long raw = ADC; 
  
  // 1. FILTRU ALPHA
  senzor_filtrat = (raw * 5UL + senzor_filtrat * 95UL + 50UL) / 100UL;
  
  if (!calibrare_gata) {
    counter_esantioane++;
    if (senzor_filtrat > senzor_max_calibrat) {
      senzor_max_calibrat = senzor_filtrat;
    }
    pwm_target = 30; 
  } 
  else {
    // 2. CURBA PATRATICA
    unsigned long squared = senzor_filtrat * senzor_filtrat;
    unsigned long calcul = 5UL + (squared / divizor_gamma);
    
    // 3. SATURARE
    if (calcul < 5UL)   calcul = 5UL;
    if (calcul > 100UL) calcul = 100UL;
    
    // 3. FILTRU DE HISTEREZIS
    uint8_t noul_pwm = (uint8_t)calcul;
    int diferenta = (int)noul_pwm - (int)pwm_target;
    
    // Actualizăm doar dacă modificarea e mai mare de 3 unități
    if (diferenta > 3 || diferenta < -3) {
      pwm_target = noul_pwm;
    }
  }
  
  OCR1A = pwm_target; 
}

// ==========================================================
// EXECUTIE IN PARALEL PE D3, D4, D5 (Adaptare de Impedanta Software)
// ==========================================================
ISR(TIMER1_OVF_vect) {
  DDRD &= ~MASCA_PINI; 
}

ISR(TIMER1_COMPA_vect) {
  if (OCR1A < 100) {
    DDRD |= MASCA_PINI;  // Masa fortata (Ecran stins)
  }
}

const int onOff = 6;
const int dir = 7;
const int onOffi = 8;
const int diri = 9;
const int high = 10;

const int blink1 = 3;
const int blink2 = 4;
const int blink3 = 5;

void setup() {
  pinMode(high, OUTPUT);
  digitalWrite(high, HIGH);
  pinMode(onOff, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(onOffi, INPUT);
  pinMode(diri, INPUT);
  pinMode(blink1, OUTPUT);
  pinMode(blink2, OUTPUT);
  pinMode(blink3, OUTPUT);
  
}

void loop() {
  //digitalWrite(fw, HIGH);
  if(digitalRead(diri) == HIGH && digitalRead(onOffi) == HIGH){
    digitalWrite(dir, HIGH);
    digitalWrite(blink1, HIGH);
    digitalWrite(blink2, LOW);
    digitalWrite(blink3, LOW);
    }
  else if(digitalRead(diri) == LOW && digitalRead(onOffi) == HIGH){
    digitalWrite(dir, LOW);
    digitalWrite(blink2, HIGH);
    digitalWrite(blink1, LOW);
    digitalWrite(blink3, LOW);
  }else{
    digitalWrite(blink2, LOW);
    digitalWrite(blink1, LOW);
    digitalWrite(blink3, HIGH);
  }
  if(digitalRead(onOffi) == HIGH){
    digitalWrite(onOff,HIGH); 
    delay(1); 
    digitalWrite(onOff,LOW); 
    delay(1);
    } 
}

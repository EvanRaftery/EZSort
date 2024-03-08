const int onOff = 7;
const int dir = 6;
const int sleep = 8;

const int onOffi = A3; //8;
int diri = 1;
const int high = A1;// 10;

const int blink1 = 3;
const int blink2 = 4;
const int blink3 = 5;
int count = 0;

void setup() {
  pinMode(high, OUTPUT);
  digitalWrite(high, HIGH);
  pinMode(onOff, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(onOffi, INPUT);
  pinMode(sleep, OUTPUT);
  digitalWrite(sleep, HIGH);
  //pinMode(diri, INPUT); No longer needed, one direction so I will hard code it for now.
  pinMode(blink1, OUTPUT);
  pinMode(blink2, OUTPUT);
  pinMode(blink3, OUTPUT);
  diri = 1; // Set low if belt goes wrong 

  Serial.begin(9600);
  
  
}

void loop() {
  //digitalWrite(fw, HIGH);
  //Serial.println(diri);
  //Serial.println(analogRead(onOffi));
  int store = digitalRead(onOffi);

  //Serial.print("onOffi: ");
  //Serial.println(store);
  if(diri == 1 && store == HIGH){//if(digitalRead(diri) == HIGH && digitalRead(onOffi) == HIGH){
    //Serial.println("Good Flag");
    digitalWrite(dir, HIGH);
    digitalWrite(blink1, HIGH);
    digitalWrite(blink2, LOW);
    digitalWrite(blink3, LOW);
    }
  else if(diri == 0 && store == HIGH){//digitalRead(onOffi) == HIGH){//else if(digitalRead(diri) == LOW && digitalRead(onOffi) == HIGH){
    //Serial.println("Bad Flag1");
    digitalWrite(dir, LOW);
    digitalWrite(blink2, HIGH);
    digitalWrite(blink1, LOW);
    digitalWrite(blink3, LOW);
  }else{
    //Serial.println("Bad Flag2");
    digitalWrite(blink2, LOW);
    digitalWrite(blink1, LOW);
    digitalWrite(blink3, HIGH);
  }
  if(store){//digitalRead(onOffi) == HIGH){
    Serial.println("FLAG");
    for(int i = 0; i < 600; i++){
      digitalWrite(onOff,HIGH); 
      delay(2); 
      digitalWrite(onOff,LOW); 
      delay(2);
      }
    } 
}

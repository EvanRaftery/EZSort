 #include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);

MFRC522::MIFARE_Key key; 

const int onOff = 7;
const int dir = 6;
const int sleep = 8;


//const int diri = 5; //Legacy I believe. Might beable to delete
const int high = 2; 


const int onOffi = A0;//4; // BELT
const int binval1 = A1; // Binary value representing destination bin
const int binval2 = A2;

const int nanoB = A3; // Output that tells NanoB when to go on

const int blinkr = 3; //D3;
const int blinky = 4;   //D4;
const int blinkg = 5;   //D5;

byte uid[4];

byte uid0;
byte uid1;
byte uid2;
byte uid3;
byte uidL_Init[4];
byte uidL_Run[4];
byte store;

int pos;
int goPos0;
int prevPos;
//int goPos1;

int uidFlag;
int uidInitFlag;

int flag;

unsigned long timerSpin1 = 0;
unsigned long timerSpin2 = 0;
unsigned long timerCat1 = 0;
unsigned long timerCat2 = 0;
unsigned long bDelay = 15000.0;

void setup() {
  pinMode(high, OUTPUT);
  digitalWrite(high, HIGH);
  pinMode(onOff, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(sleep, OUTPUT);
  digitalWrite(sleep,HIGH);
  digitalWrite(dir, LOW);
  

  // 3 Pi comm pins
  pinMode(onOffi, INPUT);
  pinMode(binval1, INPUT);
  pinMode(binval2, INPUT);

  // NanoB Control pin
  pinMode(nanoB, OUTPUT);

  
  
  //******************************pinMode(diri, INPUT);
  
  pinMode(blinkr, OUTPUT);
  pinMode(blinky, OUTPUT);
  pinMode(blinkg, OUTPUT);
  Serial.begin(9600);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(SS_PIN, RST_PIN);
  uid0 = 0x62; //98 Red
  uid1 = 0x40; //64 Purple
  uid2 = 0xA0; //160 Orange
  uid3 = 0x63; //99 White
  uidL_Init[0] = uid0;
  uidL_Init[1] = uid1;
  uidL_Init[2] = uid2;
  uidL_Init[3] = uid3;
  
  uidInitFlag = 0;
  flag = 1;

  //goPos0 = 2;
  digitalWrite(nanoB, LOW);
  
}

void loop() {    
  digitalWrite(nanoB, LOW);
  int binPos1 = digitalRead(binval1);
  int binPos2 = digitalRead(binval2);

  if(!(digitalRead(onOffi))){
    //prevPos = goPos0;
    if(goPos0 != (binPos2 * 2 + binPos1)){flag = 1;}
    goPos0 = binPos2 * 2 + binPos1;
  }else{
    //Turn on LEDS accordingly
    if(binPos1){
      digitalWrite(blinkg, HIGH);
    }else{
      digitalWrite(blinkg, LOW);
    }
    if(binPos2){
      digitalWrite(blinkr, HIGH);
    }else{
      digitalWrite(blinkr, LOW);
    }
  }
  
  /*Serial.print(prevPos);
  Serial.print(" : ");
  Serial.print(pos);
  Serial.print(" : ");
  Serial.println(goPos0);*/

  
  if(pos != prevPos && pos == goPos0 && flag){
    Serial.println("FLAG IN CONDITIONAL");
    digitalWrite(nanoB, HIGH);
    delay(10); // Vary time
    digitalWrite(nanoB, LOW);
    timerSpin1 = millis();
    flag = 0;
  }
  //}

   if( (millis() - timerSpin1) > bDelay && (millis() - timerCat1) > bDelay && !(digitalRead(onOffi))){
    Serial.println("FLAG IN CONDITIONAL");
    digitalWrite(nanoB, HIGH);
    delay(10); // Vary time
    digitalWrite(nanoB, LOW);
    //flag = 0;
    timerSpin1 = millis();
   }
  /*LED LOGIC*/
  
  if(rfid.PICC_IsNewCardPresent()){
    rfid.PICC_ReadCardSerial();
  
  for (byte i = 0; i < 4; i++) {
    uid[i] = rfid.uid.uidByte[i];
  }

  // Halt PICC
  rfid.PICC_HaltA();

  // Stop encryption on PCD
  rfid.PCD_StopCrypto1();
  }

  if(!uidInitFlag){
    int value;
    int adjust;
    for(int j = 0; j < 4; j++){
      if(uidL_Init[j] == *uid){
        value = j;  
        }
      }
    for(int i = 0; i < 4; i++){
      adjust = i + value;
      if(adjust > 3){adjust -= 4;}
      uidL_Run[i] = uidL_Init[adjust];
      Serial.println(uidL_Run[0]);
      Serial.println(uidL_Run[1]);
      Serial.println(uidL_Run[2]);
      Serial.println(uidL_Run[3]);
      Serial.println(" ");
       }
    //Serial.println(value);
    uidInitFlag = 1;
    pos = 0; 
    }
  
  Serial.print(goPos0);
  Serial.print("  ");
  Serial.println(pos);
  prevPos = pos;
  if(*uid != uidL_Run[pos]){
  for(int j = 0; j < 4; j++){
    if(uidL_Run[j] == *uid){
      pos = j;  
      }
    }
  }

  if(pos == goPos0){
    digitalWrite(onOff, LOW);
    delay(1);
  }else{
     timerCat1 = millis();
     if((pos == 0 && goPos0 == 3) || ((pos - goPos0) == 1)){digitalWrite(dir, HIGH);
     Serial.println("HIGH");}
     else{digitalWrite(dir, LOW);
     Serial.println("LOW");
     }
        //Serial.println(goPos0);
        digitalWrite(onOff,HIGH); 
        //delay(0.5); 
        delay(15);
        digitalWrite(onOff,LOW); 
        //delay(0.5);
        delay(1);
        //Serial.print("I");
         //}
      //digitalWrite(dir, HIGH);
  }
  
}

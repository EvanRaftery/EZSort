#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);

MFRC522::MIFARE_Key key; 

const int onOff = 6;
const int dir = 7;
//const int onOffi = 8;
//const int diri = 9;
const int onOffi = 4;
const int diri = 5;
//const int high = 10;
const int high = 2;

//const int blink1 = 3;
//const int blink2 = 4;
//const int blink3 = 5;
//const int blink2 = 0;
//const int blink3 = 1;

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
int goPos1;

int uidFlag;
int uidInitFlag;

void setup() {
  pinMode(high, OUTPUT);
  digitalWrite(high, HIGH);
  pinMode(onOff, OUTPUT);
  pinMode(dir, OUTPUT);
  digitalWrite(dir, LOW);
  pinMode(onOffi, INPUT);
  pinMode(diri, INPUT);
  //pinMode(blink1, OUTPUT);
  //pinMode(blink2, OUTPUT);
  //pinMode(blink3, OUTPUT);
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

  goPos0 = 3;

  
  
}

void loop() {
  /*switch(goPos1){
    case 1: DigitalRead(high){Second switch} 
    }*/
  
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
    Serial.println(value);
    uidInitFlag = 1;
    pos = 0; 
    }
  
  Serial.print(uid[0]);
  Serial.print("  ");
  Serial.println(uid0);

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
    //digitalWrite(dir, HIGH);
    //if(abs(goPos0 - pos) == 1){
      // Switch greater than signs if performing wrong
      //if(goPos0 - pos < 0){
        //digitalWrite(dir, LOW);
        //}

      //}
     //for(int i = 0; i < 50; i++){
     if((pos == 0 && goPos0 == 3) || ((pos - goPos0) == 1)){digitalWrite(dir, HIGH);}
     else{digitalWrite(dir, LOW);}
        digitalWrite(onOff,HIGH); 
        delay(0.1); 
        digitalWrite(onOff,LOW); 
        delay(0.1);
        //Serial.print("I");
         //}
      //digitalWrite(dir, HIGH);
  }
  
  /*if (uid[0] == uid0){
    if(!uidFlag){
    if(digitalRead(diri) == HIGH){digitalWrite(dir, LOW);} else {digitalWrite(dir, HIGH);}
    //digitalWrite(onOff,HIGH);  IF DRIFTING UNCOMENT AND PUT INTO LOOP FOR REVERSE
    //delay(1);
    //digitalWrite(onOff, LOW);
    //delay(1);
    uidFlag = 1;
    }
    digitalWrite(onOff, LOW);
    delay(1);
    }else{uidFlag = 0;}*/


  /*if(uid[0] != uid0){
    digitalWrite(onOff,HIGH); 
    delay(1); 
    digitalWrite(onOff,LOW); 
    delay(1);
    } */
}

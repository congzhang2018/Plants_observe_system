
void setup()
{
  Serial.begin(9600);
  pinMode(A0, INPUT); 
}

void loop()
{
  int s = analogRead(A0); 
  Serial.println(s);
  delay(1000);
  
}


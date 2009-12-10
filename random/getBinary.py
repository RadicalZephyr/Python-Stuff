def getbinary(number):
   k =''
   while(number):
      if number%2==1:
         k='1'+k
         number = number/2
      else:
         k='0'+k
         number = number/2
         
   print k

getbinary(int(raw_input()))


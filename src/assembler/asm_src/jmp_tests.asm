; zero jump check
load_byte 47d
mov a,t
load_byte 47d
mov b,t
xor
jmp_z &success

load_byte 99d
output ; if 99 is outputted, we failed

success:
  load_byte 100d
  output

; not zero jump check
load_byte 48d
mov a,t
load_byte 47d
mov b,t
xor
jmp_nz &success2

load_byte 101d
output  ; if 101 is outputted, we failed

success2:
  load_byte 102d
  output


; carry jump check
load_byte 200d
mov a,t
load_byte 100d
mov b,t
add
jmp_c &success3

load_byte 103d
output ; if 103 is outputted, we failed

success3:
  load_byte 104d
  output

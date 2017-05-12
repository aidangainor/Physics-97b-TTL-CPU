load_byte 0d
mov a,t
load_byte 1d
mov b,t

loop_start:
  add
  mov a,t
  output
  add
  mov b,t
  output
  jmp_un &loop_start

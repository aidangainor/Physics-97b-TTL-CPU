; Makes a visual display for the B register where lights increment for every other light

load_byte 1d ;
mov a,t ;
load_byte 4d ;
mov b,t ;
add ;
mov b,t ;
load_byte 16d ;
mov a,t ;
add ;
mov b,t ;
load_byte 64d ;
mov a,t ;
add ;
mov b,t ;
load_byte 255d ;
mov a,t ;
add ;
mov b,t ;
jmp_un 0d ;

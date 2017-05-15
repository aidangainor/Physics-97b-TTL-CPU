; Makes a visual display for b Register and OUTPUT simulating a "Power Guage"
; LEDs (b) shine at 1,3,7,15,31,63,127,255
; Different cycle times for LED 1-3 [15], 4-6 [30], 7-8 [60]
; Different number displayed on OUTPUT rather than b
; OUTPUT ranges from 1-100, b 1-255

poweron:

load_byte 0d 
output 
nop
mov i,t 			;Start Cycle Counter at 0
load_byte 4d			;Cycle 4 times
mov c,t				;Store Cycle Count

lowpower:

load_byte 1d 			;Grab 1 [00000001] (1 = LED light on; 0 = LED light off)
output
mov b,t 			;b = 00000001 (1)
output 				;7seg = 1
nop
load_byte 2d 			;Grab 2 [00000010]
mov a,t 
add 				;Add 1 + 2
mov b,t 			;b = 00000011 (3)
output 				;7seg = 3
nop
load_byte 4d 			;Grab 4 [00000100]
mov a,t 
add 				;Add 4 + 3
mov b,t 			;b = 00000111 (7)
output  			;7seg = 7
nop
push				;Store b Register (7)
push
push				;Into 3rd Element of Stack

inc ij 				;i = i + 1 (Cycle Counter plus one)
mov t,i 			;Move i to t (No i to b command)
mov b,t 			;Move t to b (Prep Cycler)
mov t,c 			;Grab cycle counter
mov a,t 			;Prep cycle
xor				;If i = C; 0. If i != C; 1.
jmp_nz &lowpower		;Loop ends at i = C; 4


load_byte 0d			;Reset Cycle Counter
mov i,t 			;Store Cycle Counter
load_byte 8d			;Cycle 8 times
mov c,t				;Store Cycle Count

midpower:

pop				;Bring back b Register (7)
pop
pop				;From 3rd element
mov b,t 			;b = 00000111
output
nop
load_byte 8d 			;Grab 8 [00001000]
mov a,t 
add 				;Add 7 + 8
mov b,t 			;b = 00001111 (15)
output 				;7seg = 15
nop
load_byte 16d 
mov a,t 
add 				;Add 15 + 16
mov b,t 			;b = 00011111 (31)
push				;Store b Register (31)
push				;Into 2nd Element of Stack
output 				;7seg = 31
nop
load_byte 32d 
mov a,t 
add 				;Add 31 + 32
mov b,t 			;b = 00111111 (63)
output 				;7seg = 63
nop

inc ij	 			;i = i + 1 (Cycle counter plus one)
mov t,i 			;Move i to t (No i to b command)
mov b,t 			;Move t to b (Prep Cycler)
mov t,c 			;Grab cycle counter
mov a,t 			;Cycle Counter can be XORed with Cycle Count
xor				;If i = C; 0. If i != C; 1.
jmp_nz &midpower		;Loop ends at i = C; 8

load_byte 0d			;Reset Cycle Counter
mov i,t 			;Store Cycle Counter
load_byte 12d			;Cycle 12 times
mov c,t				;Store Cycle Count

highpower:

pop				;Bring back b Register (31)
pop				;From 2nd Element of Stack
mov b,t				;b = 00011111
output				;7seg = 31
nop
load_byte 32d 
mov a,t 
add 				;Add 31 + 32
mov b,t 			;b = 00111111 (63)
output 				;7seg = 63
nop
load_byte 64d 
mov a,t 
add 				;Add 63 + 64
mov b,t 			;b = 01111111 (127)
load_byte 83d			;Power Output (83 corresponds with 127b)
output				;Display 83
nop
load_byte 128d 
mov a,t 
add 				;Add 127 + 128
mov b,t 			;b = 1111111 (255)
load_byte 99d			;Power Output (99 correspond with 255b)
output				;Display 99
nop

inc ij	 			;i = i + 1 (Cycle Counter plus one)
mov t,i 			;Move i to t (No i to b command)
mov b,t 			;Move t to b (Prep Cycler)
mov t,c 			;Grab cycle counter
mov a,t 			;Cycle Counter can be XORed with Cycle Count
xor				;If i = C; 0. If i != C; 1.
jmp_nz &highpower		;Loop ends at i = C; 12



overload:

load_byte 255d			;11111111 (255) to b Register
mov b,t				;All LEDs on in b Register
load_byte 100d			;Power at Max (100)
output				;Display Power at Max
nop				;Stall LED display on to imitate flashing on and off
nop
nop 
nop 
nop 
load_byte 0d			;00000000 (0) to b Register
mov b,t				;All LEDs off in b Register
output				;Power off (0)
nop				;Stall LED display off to imitate flashing on and off
nop
nop
nop
nop

jmp_un &overload	
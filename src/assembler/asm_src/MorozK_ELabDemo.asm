; Makes a visual display for b Register and OUTPUT simulating a "Power Guage"
; LEDs (b) shine at 1,3,7,15,31,63,127,255
; Different cycle times for LED 1-3 [15], 4-6 [30], 7-8 [60]
; Different number displayed on OUTPUT rather than b
; OUTPUT ranges from 1-100, b 1-255

poweron:

load_byte 0d 
output 
mov i,t 

load_byte 15d			;Cycle 15 times
mov c,t				;Store Cycle Count

lowpower:

load_byte 1d 
mov b,t 
output 
load_byte 2d 
mov a,t 
add 
mov b,t 
output 
load_byte 4d 
mov a,t 
add 
mov b,t 
output  
push				;Store b Register (7)

inc ij 				;i = i + 1 (Cycle Counter)
mov t,i 			;Move i to t (No i to b command)
mov b,t 			;Move t to b (Prep Cycler)
mov t,c 			;Grab cycle counter
mov a,t 			;Prep cycle
xor
jmp_nz &lowpower		;Loop ends at i = C; 15

load_byte 0d			;Reset Cycle Counter
mov i,t 			;Store Cycle Counter

midpower:

load_byte 30d			;Cycle 30 times
mov c,t				;Store Cycle Count

pop
mov b,t 
load_byte 8d 
mov a,t 
add 
mov b,t 
output 
load_byte 16d 
mov a,t 
add 
mov b,t 
output 
push				;Store b Register (31)
load_byte 32d 
mov a,t 
add 
mov b,t 
output

midcycle:

inc ij	 			;i = i + 1
mov t,i 			;Move i to t (No i to b command)
mov b,t 			;Move t to b (Prep Cycler)
mov t,c 			;Grab cycle counter
mov a,t 			;Cycle Counter can be XORed with Cycle Count
xor
jmp_nz &midpower		;Loop ends at i = C; 30

load_byte 0d			;Reset Cycle Counter
mov i,t 			;Store Cycle Counter

highpower:

load_byte 60d			;Cycle 60 times
mov c,t				;Store Cycle Count

pop
load_byte 32d 
mov a,t 
add 
mov b,t 
output
load_byte 64d 
mov a,t 
add 
mov b,t 
load_byte 83d			;Power Output (83 corresponds with 127b)
output				;Display 83
load_byte 128d 
mov a,t 
add 
mov b,t 
load_byte 99d			;Power Output (99 correspond with 255b)
output				;Display 99

highcycle:

inc ij	 			;i = i + 1
mov t,i 			;Move i to t (No i to b command)
mov b,t 			;Move t to b (Prep Cycler)
mov t,c 			;Grab cycle counter
mov a,t 			;Cycle Counter can be XORed with Cycle Count
xor
jmp_nz &highpower		;Loop ends at i = C; 60



overload:

load_byte 255d			;255 in Binary to b Register
mov b,t				;All LEDs on in b Register
load_byte 100d			;Power at Max (100)
output				;Display Power at Max
nop				;Stall LED display on to imitate flashing on and off
nop
nop 
nop 
nop 
load_byte 0d			;0 in Binary to b Register
mov b,t				;All LEDs off in b Register
output				;Power off (0)
nop				;Stall LED display off to imitate flashing on and off
nop
nop
nop
nop

jmp_un &overload	
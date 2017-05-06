; Add the numbers 75 and 65 in decimal and output onto data bus
load_byte 75d ; T = 75
mov a,t ; A = T
load_byte 65d ; T register
mov b,t ; B = T
add ; T = A + B

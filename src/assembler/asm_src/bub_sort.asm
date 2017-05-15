
  ;start the double loop where the top layer of the for loop always starts
pop
push
push
  ;go back to start of the array
load_byte 32d     ; load T register w/ 32,
mov i,t           ; I = 32
load_byte 0d
move j,t
push
;put index n into register c
load_ind
mov c,t
mov b,t
inc ij
load_ind
mov a,t
sub
jmp_nn

  ;hold index n at c
  ;
  ;we want the bigger number to float up
  ;solve how to switch within the array
  mov


  ;count elements in the array
load_byte 0d
move a,t
load_byte 1d
move b,t

load_ind
move a,t
load_byte 255d
move b,t
and
jmp_nz 42d

  ;

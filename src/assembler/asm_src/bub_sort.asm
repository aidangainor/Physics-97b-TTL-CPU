

  ; start array at 8192
load_byte 32d     ; load T register w/ 32,
mov j,t           ; I = 32

  ;load arrays with any values from 0-254s
  ;load first index
load_byte 22d      ; T = 22
store_ind         ; array[0] = 22
inc ij            ; J = J + 1

  ;load second index
load_byte 40d      ; T = 40
store_ind         ; array[1] = 40
inc ij            ; J = J + 1

  ;load third index
load_byte 100d      ; T = 100
store_ind         ; array[2] = 100
inc ij            ; J = J + 1

  ;load final index
load_byte 255d      ; T = 255
store_ind         ; array[3] = 255
inc ij            ; J = J + 1

    ;begin construction of loop using the stack to hold the size of the array
  ;go back to beginning of array
load_byte 32d     ; load T register w/ 32,
mov j,t           ; I = 32
load_byte 0d
move i,t
push ; push 0 to stack
  ;check if empty array by xoring the current index and 255 which we state as the last array symbol
load_ind      ;check index of array, starting at 1
move a,t      ;move array[n] to a
load_byte 255d
move b,t      ;move 255 to b
xor           ;xor, if 255, output will be 0
jmp_z 59d     ;we have reached the end of the array and thus have finished counting

  ;add 1 to count which is held in stack
pop
mov a,t
load_byte 1d
move b,t
add
push
inc ij
jmp_nz 43d

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

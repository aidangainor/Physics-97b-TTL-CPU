
; load arrays with any values from 0-254s

load_byte 32d     ; load T register w/ 32,
mov i,t           ; I = 32
; start array at 8192

  ;load first index
load_byte 22d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array[0] = 0
inc ij            ; J = J + 1
  ;load second index
load_byte 40d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array[0] = 0
inc ij            ; J = J + 1
  ;load third index
load_byte 100d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array[0] = 0
inc ij            ; J = J + 1
  ;load fourth index
load_byte 16d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array[0] = 0
inc ij            ; J = J + 1
  ;load fifth index
load_byte 3d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array[0] = 0
inc ij            ; J = J + 1
  ;load sixth index
load_byte 77d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array[0] = 0
inc ij            ; J = J + 1
  ;load final index
load_byte 255d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array[0] = 0
inc ij            ; J = J + 1
  ;go back to beginning of array
load_byte 32d     ; load T register w/ 32,
mov i,t           ; I = 32
load_byte 0d
move j,t
push ; push 0 and start counting
  ;check if empty array by anding the current index and 255 which we state as the last array symbol
load_ind
move a,t
load_byte 255d
move b,t
and
jmp_z 59d
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






  ;count size of array
push to stack size of array

;; goal is for biggest to float up to biggest on
;go through loop
if not zero
push identical value to top of stack
store first into c
switch



;output






load_byte 253d    ; load decimal value 253 to T register, this plus our first 2 increments + 253 = 255 (array size)
mov a,t           ; A = 253

;;;; load into RAM one value and increment to next register



; end array loading

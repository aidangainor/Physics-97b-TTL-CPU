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
mov i,t
push ; push 0 to stack

  ;check if empty array by xoring the current index and 255 which we state as the last array symbol
load_ind      ;check index of array, starting at 1
mov a,t      ;move array[n] to a
load_byte 255d
mov b,t      ;move 255 to b
xor           ;xor, if 255, output will be 0
jmp_z 53d     ;we have reached the end of the array and thus have finished counting

  ;add 1 to count which is held in stack
pop           ;pops count from stack
mov a,t       ;moves it to register a
load_byte 1d  ;loads 1 to t
mov b,t      ;which is then moved to b
add           ;and we add them so that the count goes up by 1
push          ;to which we then push back to the stack
inc ij        ;and we increment ij in order to scan the next index in the array
jmp_nz 35d    ;and we go back to the start of checking for 255


  ;output count
pop
output

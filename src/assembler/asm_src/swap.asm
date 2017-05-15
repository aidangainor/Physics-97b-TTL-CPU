call &to_index_zero

  ;load first index
load_byte 123d       ; T = 123
store_ind           ; array[0] = 100
inc ij              ; J = J + 1
output

  ;load second index
load_byte 45d       ; T = 45
store_ind           ; array[1] = 40
inc ij              ; J = J + 1
output

;turing end file symbol
load_byte 255d       ; T = 255
store_ind           ; array[255] = 255
inc ij              ; J = J + 1
output

call &to_index_zero
load_ind
mov a,t ; a holds 100
inc ij
load_ind
mov b,t ; b holds 40
call &swap
call &to_index_zero
call &show_array_contents
halt

swap: ;puts A before B in the index
  mov t,b
  mov c,t ;c stores b
  mov t,i
  mov b,t ;b stores i
  mov t,a
  mov i,t ;i stores a
  load_byte 11111111b
  mov a,t ;add 255 to subtract 1 through twos complement
  add ; t = index-1
  mov a,t ; a = index-1
  mov t,i ; t = a
  mov b,t ; b = a
  mov t,a ; t = index-1
  mov i,t ; i = index-1
  mov t,b ; t = a
  store_ind ; load index-1 with a
  inc ij
  mov t,c
  store_ind
  return

to_index_zero:
  load_byte 32d     ; load T register w/ 32,
  mov j,t           ; I = 32
  load_byte 0d
  mov i,t
  return

show_array_contents:
  load_ind
  mov b,t
  output
  inc ij
  load_byte 255d
  mov a,t
  xor
  jmp_nz &show_array_contents
  return

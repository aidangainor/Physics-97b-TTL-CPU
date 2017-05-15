; Lets store an array of size 255 at the first RAM address, which is 8192
; Since we have 8 bit registers only, store the value 32 in reg J
; J is highest 8 bits on address lines and I is lowest 8 bits on address lines
; This works out since I + J is reset on startup and 32 << 8 = 8192

load_byte 32d     ; load T register w/ decimal value 32,
mov j,t           ; J = 32

load_byte 0d      ; register T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array_of_primes_booleans[0] = 0
inc ij            ; 8192 is start of array, so we are now going to 8193 or array index 1
store_ind         ; array_of_primes_booleans[1] = 0

load_byte 255d    ; load decimal value 255 to T register, so we will stop our array when I = 255
mov a,t           ; A = 255, we will check if I = A and stop array init there

array_init_start:
  inc ij                      ; I = I + 1
  mov t,i                     ; Move I register (lower byte) to T (T = I)
  mov b,t                     ; Move T register to B register (B = T)
  load_byte 1d                ; let the value 1 indicate "True", so by default
  store_ind
  xor                         ; T = A xor B, this is basically an equality check
                              ; If I == 255, that means we are done initializing our array so lets break loop
  jmp_nz &array_init_start    ; Go back to loop start, and stop looping when I == 255

load_byte 2d      ; We are going to reset the I register to 2, why thought? It is because 2 is the first prime number
mov i,t           ; I = 2, since I is basically a reference to a number 0 thru 255
                  ; The value in RAM pointed by memory address in IJ is either 0 for not prime, and 1 for prime

mov t,i
mov a,t           ; Load a and b with current prime found, and compute the square
mov b,t

call &multiply_subroutine
jmp_c &outside_loop_end ; If carry bit is set, then that means result of current_prime * current_prime > 255





; We are done computing primes, so now print them all out
outside_loop_end:
  load_byte 2d    ; Reset I to 2, since we know 2 is prime
  mov i,t

  print_loop:
    load_ind        ; Load array value into T register
    mov a,t
    load_byte 1d
    mov b,t
    xor
    jmp_nz &check_if_array_end   ; If value in array != 1, then don't print

    call print_subroutine        ; If i == 0, then we print the prime number

    check_if_array_end:
      inc_ij
      ; Check if array end section by seeing if I == 255
      load_byte 255d
      mov b,t
      mov t,i
      mov a,t
      xor                   ; Check if I == 255
      jmp_nz &print_loop    ; Keep printing primes until I == 255
      halt

print_subroutine:
  mov t,i                 ; Prime number is in I register (index into array)
  output
  return


; Multiply two numbers stored in the ALU A and B input registers
; Output is stored in A register
; Sums are accumulated in A register while B register is decremented
multiply_subroutine:
  mov t,a                     ; T = A, we need to save T in C register
  mov c,t                     ; C = T aka C = A, or in other words we are saving the A input into C register
  load_byte 0d                ; Sum = 0
  mov a,t                     ; Our sum is stored in A, so we initialize sum variable to 0

  multiply_loop:
    ; Check if B == 0 section
    load_byte 0d                ; T = 0, this is for the check that B == 0
    mov a,t                     ; A = 0
    xor                         ; check if B == 0
    jmp_z &return_from_loop

    ; Decrement B section
    load_byte 255d              ; 255 = -1 following 2's complement representation of negative numbers
    mov a,t                     ; A = -1
    add                         ; B = B + (-1)

    mov t,b
    push                        ; We don't have enough registers so save B register onto stack (it was stored as temp in T)

    ; Accumulate sum section
    mov t,c                     ; T = C, in other words we are grabbing original value of A from C register
    mov b,t                     ; B = T aka B = C
    add                         ; T = A + B
    mov a,t                     ; Sum is stored in A, so sum = sum + A input

    pop
    mov b,t                     ; Pop original value of B from stack back into B
    jmp_un &multiply_loop       ; Loop!

  return_from_loop:
    return                      ; Pop program counter from stack and return to our caller's location

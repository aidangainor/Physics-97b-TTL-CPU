; Lets store an array of size 255 at the first RAM address, which is 8192
; Since we have 8 bit registers only, store the value 32 in reg I
; This works out since I + J is reset on startup and 32 << 8 = 8192

load_byte 32d     ; load T register w/ 32,
mov i,t           ; I = 32

load_byte 0d      ; T = 0, we note the numbers 0 and 1 are not prime, 0 represents "False"
store_ind         ; array_of_primes_booleans[0] = 0
inc ij            ; 8192 is start of array, so we are now going to 8193 or array index 1
store_ind         ; array_of_primes_booleans[1] = 0

load_byte 253d    ; load decimal value 253 to T register, this plus our first 2 increments + 253 = 255 (array size)
mov a,t           ; A = 253

array_init_start:
  inc ij                      ; J = J + 1
  mov t,j                     ; Move J register (lower byte) to T (T = J)
  mov b,t                     ; Move T register to B register (B = T)
  load_byte 1d                ; let the value 1 indicate "True", so by default
  xor                         ; T = A xor B, this is basically an equality check
                              ; If j == 255, that means we are done initializing our array so lets break loop
  jmp_nz &array_init_start    ; Go back to loop start, and stop looping when j == 255

load_byte 2d      ; We are going to reset the J register to 2, why thought? It is because 2 is the first prime number
mov j,t           ; J = 2


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

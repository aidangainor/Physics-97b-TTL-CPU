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

load_byte 1d      ; We are going to reset the I register to 1, why though?
                  ; It is because 2 is the first prime number, and at the start of the main loop we always increment by 1
                  ; Therefore we get 2 the first run through of the algorithm
mov b,t           ; B = 1, since B is basically a reference to a number 0 thru 255
                  ; The value in RAM pointed by memory address in IJ is either 0 for not prime, and 1 for prime

outer_main_loop:
  mov t,b           ; This is done to save original value of I register, aka current prime we are on
                    ; Currently this prime in in register B, and later on we will cross out multiples of it (if it is prime)

  mov a,t           ; Load a and b with current prime found, and compute the square
  mov b,t

  output

  push                          ; Save current prime onto stack
  call &multiply_subroutine     ; Square current prime, if > 255, we are done
  pop
  mov i,t                       ; Get back original value of I reg (current prime)

  jmp_c &outside_loop_end       ; If carry bit is set, then that means result of current_prime * current_prime > 255

  inc ij            ; Always increment I, we will never carry over to J since max number we check if prime is 255

  ; Check if I references a prime number, our first prime should be 2
  load_byte 1d      ; 1 is boolean "number is prime"
  mov b,t
  load_ind          ; Use IJ to look of array of booleans to check if this number has been marked as prime yet
  mov a,t           ; Transfer the number to A register to XOR with 1, if result = 0 then this number is marked as prime
  xor               ; if XOR result is 1, then that means number (in reg I) is not prime

  mov t,i           ; do this before we jump (in that I is always incrementing by 1)
  mov b,t

  jmp_nz &outer_main_loop   ; Re iterate main prime checking loop if this number is not prime

  ; If we reach this code here means that we are at a prime number, so cross of all multiples of it by marking them not prime
  ; For example if our first prime is 2, then we are marking all multiples of 2 as not prime
  mov a,t

  push                        ; save original value of I onto the stack, since it will be modified in multiply_subroutine
  call &multiply_subroutine   ; register a will now contain prime number squared
  pop                         ; retrieve from stack and save into T
  mov b,t                     ; we will keep multiples of prime in register a and prime number in register b
                              ; b will not be modified until beginning of outer_main_loop execution

  ; compute all multiples of first found prime number squared, and mark their corresponding index in the array as 0 (not prime)
  mov t,a                     ; Multiple of prime is always in a register in this loop, multiply subroutine stores result in a

  inner_main_loop:
    mov i,t
    load_byte 0d
    store_ind                 ; Mark multiple of prime number as not a prime number by saving at index [i] value 0
    add
    mov a,t                   ; Next prime to cross off is stored in a
    jmp_c &outer_main_loop    ; Means multiple of prime > 255, so we are done crossing out primes
    jmp_un &inner_main_loop

; We are done computing primes, so now print them all out
outside_loop_end:
  load_byte 2d    ; Reset I to 2, since we know 2 is prime
  mov i,t

  print_loop:
    load_ind        ; Load array value into T register
    mov a,t
    load_byte 1d
    mov b,t
    xor                           ; Check if prime, if it is out
    jmp_nz &check_if_array_end    ; Go to end of loop if not prime (array value != 1), in other words we jump over the step of outputting
    mov t,i                       ; Prime number is in I register (index into array)
    output

    check_if_array_end:
      inc ij
      ; Check if array end section by seeing if I == 255
      load_byte 255d
      mov b,t               ; B = 255
      mov t,i
      mov a,t               ; A = I
      xor                   ; Check if I == 255
      jmp_nz &print_loop    ; Keep printing primes until I == 255
      halt


  ; Multiply two numbers stored in the ALU A and B input registers
  ; Output is stored in A register
  ; Sums are accumulated in A register while B register is decremented

  multiply_subroutine:
    mov t,a                     ; T = A, we need to save T in C register
    mov c,t                     ; C = T aka C = A, or in other words we are saving the A input into C register

    ; The sum variable is stored at memory address 8450d
    ; Therefore J = 33 and I = 2, since 33 << 8 | 2 = 8450
    load_byte 2d
    mov i,t
    load_byte 33d
    mov j,t

    load_byte 0d                ; Product = 0
    store_ind                   ; Our sum is stored at address 8450, so we initialize multiplication product variable to 0

    inc ij                      ; Decrement variable is originally B input and stored in addr 8451
    mov t,b
    store_ind

    load_byte 2d
    mov i,t                     ; Go back to addr 8450 for memory address register

    multiply_loop:
      ; Check if B == 0 section
      load_byte 1d                ; T = 0, this is for the check that B == 1
      mov a,t                     ; A = 0
      xor                         ; check if B == 0
      jmp_z &return_from_loop

      ; Accumulate sum section
      mov t,c                     ; T = C, in other words we are grabbing original value of A from C register
      mov b,t                     ; B = T aka B = C
      load_ind                    ; Grab sum from memory address 8450
      mov a,t
      add                         ; T = A + B
      store_ind                   ; Sum is stored in 8450d in RAM

      ; Decrement B section
      inc ij                      ; decrement variable stored at addr 8451
      load_ind                    ; grab decrement variable from addr 8451
      mov b,t                     ; put decrement variable in register B
      load_byte 255d              ; 255 = -1 following 2's complement representation of negative numbers
      mov a,t                     ; A = -1
      add                         ; T = B + (-1)
      store_ind                   ; We don't have enough registers so save decrement variable, so put it back into addr 8451

      load_byte 2d
      mov i,t                     ; Go back to addr 8450 for memory address register

      jmp_un &multiply_loop       ; Loop!

    return_from_loop:
      load_ind                    ; Retrieve final product from memory addr 8450 in RAM
      mov a,t                     ; Multiplication result is in a register, move it to T so we can then move to output register
      return                      ; Return to caller's location

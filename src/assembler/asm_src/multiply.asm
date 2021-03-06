; Compute all squares up to 225 by using multiplication subroutine
; Multiply two numbers stored in the ALU A and B input registers
; Output is stored in A register
; Sums are accumulated in A register while B register is decremented


load_byte 0d
mov a,t
mov b,t

loop_start:
  push
  call &multiply_subroutine
  mov t,a
  output
  nop 50
  pop
  mov i,t
  inc ij
  mov t,i
  mov b,t
  load_byte 16d
  mov a,t
  xor
  mov t,i
  mov a,t
  jmp_nz &loop_start

halt

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
    output                      ; show sum
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
    return                      ; Go back to caller

; Multiply two numbers stored in the ALU A and B input registers
; Output is stored in A register
; Sums are accumulated in A register while B register is decremented

; call &multiply_subroutine

load_byte 3d;
mov a,t
load_byte 5d;
mov b,t

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
    ; return                      ; Pop program counter from stack and return to our caller's location
    mov t,a                     ; Multiplication result is in a register, move it to T so we can then move to output register
    output
    halt

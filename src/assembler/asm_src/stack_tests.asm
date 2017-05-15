call &output_1

load_byte 2d
output

call &output_2

load_byte 4d
output

load_byte 7d
push
load_byte 6d
push
load_byte 5d
push

pop
output
pop
output
pop
output

halt

output_1:
  load_byte 1d
  output
  return

output_2:
  load_byte 3d
  output
  return

assign a 3
assign b 5
assign c 999
assign r 0
# sum of all numbers divisible by 3
div c a
assign s _
inc s
assign t _
mul a s
assign s _
mul s t
assign s _
div s 2
assign s _
add r s
assign r _
# sum of all numbers divisible by 5
div c b
assign s _
inc s
assign t _
mul b s
assign s _
mul s t
assign s _
div s 2
assign s _
add r s
assign r _
# sum of all numbers divisible by 3 and 5
mul a b
assign d _
div c d
assign s _
inc s
assign t _
mul d s
assign s _
mul s t
assign s _
div s 2
assign s _
sub r s
assign r _
print r
exit 0
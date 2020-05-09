mul_state : multiplier sub-module state
square_state : square sub-module state

exp_reg_state : curent state of the current module 
(
0 = idle,
1 = busy_sqaure_module,
2 = wait_square_modue
3 = busy_mul_module,
4 = wait_mul_module
)

modexp_ei : exponent index (NOT SURE WHAT IS THE PURPOSE)
wren : write enabled

start_op : start operation
byte counter : bytes processed
exp_reg_opaddr : address to be written to (??) (COULD HAVE REMOVED THIS SIGNAL)

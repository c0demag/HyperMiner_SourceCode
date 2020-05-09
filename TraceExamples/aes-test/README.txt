ack_aes.facts			: ack from aes (on valid operation)
aes_byte_counter.facts		: count data block reads from xram in to aes accelerator
aes_data_out_mux.facts
aes_reg_oplen.facts		: length of the aes-key / data block
aes_reg_start.facts		: begin encryption on start = 1
aes_reg_state.facts		: accelerator state (IDLE, READ_DATA, OPERATE, WAIT or WRITE)
aes_reg_state_next.facts	: state at next time steap
aes_xram_ack.facts		: ack for data read/write from arbiter
block_counter.facts		: ctr block value
block_counter_next.facts
good_value.facts		: good = 1 if encyrption/decryption succeeds
operated_bytes_count.facts	: number of bytes processed by aes
operated_bytes_count_next.facts

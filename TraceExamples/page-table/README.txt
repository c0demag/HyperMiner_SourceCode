accesser.facts	: whether page is accessed
ack_r.facts	: xram read ack from mmu
ack_w.facts	: xram write ack from mmu



# the testing is done over three regions in the memory i.e for 3 page table entry.
# each page table entry corrensponds to 2048 words in memory.

rd_enabled_0.facts	: (1 - read enabled in [0-2047], 0 read disbled in this region)
rd_enabled_1.facts	: same as above for region 1
rd_enabled_2.facts	

read_succeed.facts	: whether read succeeds

wr_enabled_0.facts : if 1 write is allowed by user process in [0-2047]
wr_enabled_1.facts : "
wr_enabled_2.facts : "

write_succeed.facts

wr_addr.facts	: write address from xiommu


# not sure about these will (to be udpdated after looking up RTL code)
ia_addr_reg.facts	
ia_reg_next.facts	
ia_rwn_reg.facts	
ia_src_next.facts	

illegal_rd.facts	
illegal_src.facts	
illegal_wr.facts	

pc_ia_reg.facts	
pt_in_rd_range.facts	
pt_in_wr_range.facts	
pt_rd_reg_use.facts	
pt_wr_reg_use.facts	
rd_addr.facts	

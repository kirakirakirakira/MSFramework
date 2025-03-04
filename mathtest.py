# filter1=Filter1(100,200)
# bucketArray=BucketArray(50,25,272,7)
filter1_d=100
filter1_w=200
filter1_ct=8
flow_id_size=32
simi_size=4
timestamp_size=10
filter2_main_num=50
filter2_alter_num=25
cm_d=272
cm_w=7
cm_ct=16
total_bit=filter1_d*filter1_w*filter1_ct+filter1_d*flow_id_size+filter1_d*simi_size+(filter2_main_num+filter2_alter_num)*(cm_d*cm_w*cm_ct+flow_id_size+simi_size+timestamp_size)
total_KB=total_bit/8//1024
print("共占用%dKB"%total_KB)
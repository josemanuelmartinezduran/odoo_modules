def pre_process_csv (in_csv, out_csv):

	f_pre_csv = open(in_csv, "r")
	pre_data = f_pre_csv.read()
	splited_pre_csv = pre_data.split ('\"')

	for x in range(0,len(splited_pre_csv)):
		if x%2 == 1:
			splited_pre_csv[x] = splited_pre_csv[x].replace("\n", " <br>")
			splited_pre_csv[x] = splited_pre_csv[x].replace(",", "&#44;")

	f_final_csv = open(out_csv, "w")


	for x in range(0,len(splited_pre_csv)):
		f_final_csv.write (splited_pre_csv[x])



		

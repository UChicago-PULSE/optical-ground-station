from Pol_Measurement_Class import Pol_Measurement

file_path = r"C:\Users\juani\Personal\CubeSat\Polarimeter Data\Sample_polarimeter.csv"
measurement_1 = Pol_Measurement("Measure 1", file_path)

#print(measurement_1.data)
#print(measurement_1.time_to_milliseconds())
#print(measurement_1.average("S 0 [mW]"))
#print(measurement_1.average("Hello"))
#print(measurement_1.stdev("S 0 [mW]"))

key_list = measurement_1.data_keys
print(key_list)

for i in range(len(key_list)):
    print(key_list[i])
    print(measurement_1.average(key_list[i]))
    print(measurement_1.stdev(key_list[i]))
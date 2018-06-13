#!/usr/bin/python3
#-*- coding: utf8 -*-


import os,sys
import wave
import numpy as np

desire_len = 20480

def main():
	input_file = sys.argv[1]
	wav = wave.open(input_file)

	print ('channel:', wav.getnchannels())


	channel = wav.getnchannels() 
	sampwidth = wav.getsampwidth() 
	framerate = wav.getframerate()

	
	if channel != 1 or sampwidth != 2 or framerate != 16000:
	    print ('channel:',channel, 'sampwidth:', sampwidth, 'rate:',framerate)
	    print('only mono 16k/samples 16bits suported')
	    exit(1)


	print ('frames:', wav.getnframes())
	frames_data = wav.readframes(wav.getnframes())
	#print (frames_data[10000:10100])
	data = np.fromstring(frames_data, dtype=np.int16)
	print (data[10000:10100])
	start, end = get_loudest_section(data, desire_len)
	print (start, end)


	if len(sys.argv) > 2:
		out_file_name =  sys.argv[2]
	else:
		out_file_name = input_file[:-4] + '_fixed_20480.wav'

	wav_out = wave.open(out_file_name, 'wb')
	wav_out.setnchannels(1)
	wav_out.setsampwidth(2)
	wav_out.setframerate(16000)
	#wav_out.setnframes(16000)
	wav_out.writeframes(data[start:end ])
	wav_out.close()






def get_loudest_section(data, desire_len):
	if len(data) < desire_len:
		return (0,len(data))


	start, end, max_sec_sum, max_start, max_end = 0,0,0,0,0


	sec_sum = np.int32(data[start])


	while end + 1 < len(data):
		end = end + 1
		if (end - start ) >= desire_len: 
			sec_sum -= abs(data[start])
			start = start + 1


		sec_sum += abs(data[end])
		if max_sec_sum < sec_sum:
			#print(sec_sum)
			max_sec_sum, max_start, max_end = sec_sum, start, end

	return ( max_start, max_end)










if __name__ == '__main__':
	main()
import re

def preprocessing():	
	#turns input_file's contents into a string
	contents = input_file.read()
	#creates a regex object to detect non-alphabetic characters
	pattern = re.compile('[^A-Z]')
	#uses pattern to replace non-alphabetic characters with nothing
	contents_final = re.sub(pattern, '', contents)
	#writes to output file
	output_file.write("Preprocessing: \n" + contents_final)
	return contents_final
	
def substitution(input, key):
	subbed_string = ""
	key_char = 0
	#loops through each char in the preprocessed input
	for char in input:
		#converts each character and the corresponding key to the ASCII value via ord()
		#subtracts 65 from each, since A is 65
		#summing them and % 26 gives the number representing the encoded letter
		#adding 65 converts back to ASCII
		value = (ord(char)-65 + ord(key[key_char%16])-65)%26 + 65
		subbed_string = subbed_string + chr(value)
		key_char += 1
	#writes substituted input to file
	output_file.write("\nSubstitution: \n" + subbed_string)
	#return substituted string
	return subbed_string
	
def padding(input):
	#determines how much padding to add
	len_modulo = len(input) % 16
	#adds padding
	padded_input = input
	for x in range(0, 16-len_modulo):
		padded_input = padded_input + "A"
	#writes padded input to file, in block format
	output_file.write("\nPadding:\n")
	block_print(padded_input)
	#return padded input
	return padded_input

def shift_rows(input):
	shifted_string = ""
	#loops through each 16-char block
	for i in range(0, len(input)-15, 16):
		#uses row 1 as-is
		shifted_string += input[i:i+4]
		#adds last 3 char of row 2, then first char
		shifted_string += input[i+5:i+8] + input[i+4]
		#adds last 2 char of row 3, then first 2 char
		shifted_string += input[i+10:i+12] + input[i+8:i+10]
		#adds last char of row 4, then first 3 char
		shifted_string += input[i+15] + input[i+12:i+15]
	#writes shifted blocks to output file
	output_file.write("\nShiftRows:\n")
	#
	block_print(shifted_string)
	return shifted_string

def parity(input):
	hex_string = ""
	#loop through each character in input
	for char in input:
		#transform char-->decimal value-->binary string
		#we also drop the binary prefix, 0b, with [2:]
		binary_char = bin(ord(char))[2:]
		#count number of 'on' bits
		number_of_ones = binary_char.count('1')
		#when number_of_ones is odd:
		if (number_of_ones % 2) is 1:
			#stick a 1 on the front.
			binary_char = '1' + binary_char
		#convert binary string into hex
		hex_string += hex(int(binary_char, 2))[2:]
	output_file.write("\nParity:\n")
	hexblock_print(hex_string)
	return hex_string
			

def hexblock_print(input):
	#prints 4 pairs of two hex
	for i in range(0, len(input)-7, 8):
		output_file.write(input[i:i+2] + " " + input[i+2:i+4] + " " + input[i+4:i+6] + " " + input[i+6:i+8] + "\n")
		if (i%32) is 24:
			output_file.write("\n")

def block_print(input):
	#prints 4 characters in a row
	for i in range(0, len(input)-3, 4):
		output_file.write(input[i] + " " + input[i+1] + " " +  input[i+2] + " " + input[i+3] + "\n")
		#additional newline at the end of the 4th row
		if (i % 16) is 12:
			output_file.write("\n")
	
if __name__ == '__main__':
	#prepare our file objects
	input_file = open('input.txt')
	key_file = open('key.txt')
	output_file = open('output.txt', 'w')
	#get key
	key = key_file.readline()
	#preprocess input
	processed_string = preprocessing()
	subbed_string = substitution(processed_string, key)
	padded_string = padding(subbed_string)
	shifted_string = shift_rows(padded_string)
	parity(shifted_string)

	input_file.close()
	key_file.close()
	output_file.close()

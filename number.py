
def main():
	print '<html><head><title>Numbers</title></head><body>'
	print '<table border=1 cellpadding=9>'
	for i in range(1,100):
		doNum(i)
	print '</table>'
	print '</body></html>'
en_num = [ 'zero',
	'one',
	'two',
	'three',
	'four',
	'five',
	'six',
	'seven',
	'eight',
	'nine',
	'ten',
	'eleven',
	'twelve',
	'thirteen',
	'fourteen',
	'fifteen',
	'sixteen',
	'seventeen',
	'eighteen',
	'nineteen',
]
en_tens = [ 'twenty',
	'thirty',
	'fourty',
	'fifty',
	'sixty',
	'seventy',
	'eighty',
	'ninety',
]
	
def doNum(num):
	print ''
	print '<tr><td width=90>'
	print num
	print '</td><td>'
	if num < len(en_num): 
		print en_num[num]
	else:
		numName = en_tens[num/10-2]
		if num % 10 != 0:
			numName += '-'+en_num[num%10]
		print numName
	print '</td><td>'
	print '<p>&nbsp;'
	print '<table border=1>'
	i=0
	while i < num:
		if i%5 == 0:
			print '<tr>',
		print '<td>&#x2022;</td>',
		if i%5 == 5-1:
			print '</tr>'
		i += 1
	while i%5 != 0:
		print '<td>&nbsp;</td>',
		if i%5 == 5-1:
			print '</tr>'
		i += 1
	print '</table>'
	print '</td><td>'
	for j in range(num/5):
		print '<img src=tally5.png />',
		if j%4 == 4-1:
			print '<br>'
	for j in range(num%5):
		print '<img src=tally1.png />'
	
	print '</td></tr>'
if __name__ == '__main__':
	main()

import re

sqlwords = ["select","use","drop","delete","create","alter","modify","add","distinct","or","not","and","where","order by","insert","in","into","update","from","as","like","between","join","union","case","when","end","procedure","unique","primary","foreign","key","check","default","identity","auto_increment","values","view"]
wrongsym = ["=",";","\"","\'","`"]
def sanitizeText(enteredData):
	data = enteredData.lower()
	for w in sqlwords:
		pattern = " "+w+" "
		if(re.search(pattern,data)):
			print("Error: Invalid input")
			return ""
	for w in wrongsym:
		if(re.search(w,data)):
			print("Error: Invalid Input")
			return ""
	return enteredData

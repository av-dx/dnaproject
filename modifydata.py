def modifyCustomer():
	print("Enter the name of Customer: ")
	name = input()
	SearchCust(name)
	while (1):
		if(cur.fetchall().length() == 1):
			last_id = cur.fetchone()['LAST_INSERT_ID()']
        	id = last_id
        	con.commit()
			break;
		print("For which id do you want to modify: ")
		id = int(input())
		break;
	print("What do you want to modify? Press Enter if nothing to change for the particualr attrubute")
	

	
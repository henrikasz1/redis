# importing redis database to the code
import redis
client = redis.Redis(host='127.0.0.1', port=6379, db=0)

#Global variables
user_id = 0
acc_num = 100

def interface():
	print("Choose the task you want to be executed:"
		  "\n Register a new client - press 1"
		  "\n Register an account - press 2"
		  "\n Make a transaction - press 3"
		  "\n Clear database - press 4"
		  "\n Kill program - press 5")
	choice = input()
	return int(choice)
# register user
def registration():
	first_name = input("Enter user's name ")
	last_name = input("Enter user's last name ")
	user = {'name': first_name, 'lastName': last_name}
	client.hmset(user_id, user)
# register an account
def account():
	id = int(input("Enter user's ID "))
	while id > user_id:
		id = int(input("User has not been found. Please try again "))

	type = input("Enter the type of account (debit - press 1 / credit - press any other key) ")
	balance = input("Enter the balance ")
	if (type == '1'):
		ty = 'debit'
	else:
		ty = 'credit'
	card = {'type': ty, 'balance': balance, 'owner': id}
	client.hmset('LT'+str(acc_num), card)
# Make transaction
def transaction():
	first_acc = input('Enter the account from which will be paid ')
	second_acc = input('Enter the account which will receive money ')
	amount = int(input('Enter the amount of money which will be transferred '))
	# insired by <3 https://fabioconcina.github.io/blog/transactions-in-redis-with-python/
	p = client.pipeline()
	p.watch(first_acc, second_acc)
	if amount <= int(client.hget(first_acc, 'balance')): # or ('credit' in client.hget(first_acc, 'type')):
		consists = p.exists(first_acc, second_acc)
		if consists:
			p.multi()
			p.hincrby(second_acc, 'balance', amount)
			p.hincrby(first_acc, 'balance', -amount)
			p.execute()
			client.sadd('transactions', 'from '+first_acc+' to '+second_acc+' -> '+str(amount)+'$')
			print('Transaction has been made')
		else:
			p.unwatch(first_acc, second_acc)
	else:
		print("Insufficient amount of money :( ")
### Main
while True:
	choice = interface()
	if choice in range (1, 6):
		if choice == 1:
			registration()
			user_id += 1
		elif choice == 2:
			account()
			acc_num += 1
		elif choice == 3:
			transaction()
		elif choice == 4:
			client.flushdb()
			input("The database has been cleared succesfully! Press any key to continue\n")
		elif choice == 5:
			break
	else:
		print("The input is incorrect, please try again!")
		input("Press any key to continue\n")
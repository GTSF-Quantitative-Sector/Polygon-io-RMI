import rmi

client = rmi.Client("HDPMwANWBOmuqurKYGJwufdUOLkjqRPN")
print(client.get_rsi("NVDA"))
print(client.get_rmi("NVDA"))

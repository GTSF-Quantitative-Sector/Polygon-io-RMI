import rmi

client = rmi.Client("API KEY Here")
print(client.get_rsi("NVDA"))
print(client.get_rmi("NVDA"))

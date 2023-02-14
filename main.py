import rmi

client = rmi.Client("API KEY HERE")
print(client.get_rsi("NVDA"))
print(client.get_rmi("NVDA"))

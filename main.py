import rmi

client = rmi.Client("API KEY HERE")
print(client.get_rmi("AAPL"))
print(client.get_rsi("AAPL"))

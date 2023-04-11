import rmi

client = rmi.Client("YOUR_API_KEY")
print(client.get_rmi("AAPL", "2022-01-01"))
print(client.get_rsi("AAPL", "2013-01-01"))

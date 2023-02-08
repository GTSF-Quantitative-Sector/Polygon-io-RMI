# Polygon-io-RMI
Fetch RMI for a stock using Polygon.io API. To use, clone this repository and run 
```
pip install -r requirements.txt
```
Sample code from `main.py` 
```
import rmi

client = rmi.Client("API KEY Here")
print(client.get_rsi("NVDA"))
print(client.get_rmi("NVDA"))

```

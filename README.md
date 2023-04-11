# Polygon-io-RMI
Calculate RMI for a stock using Polygon.io API.

## Installation
```
pip install git+https://github.com/GTSF-Quantitative-Sector/Polygon-io-RMI.git
```

## Example Usage

```python
import rmi

client = rmi.Client("API KEY Here")

print(await client.get_rsi("NVDA"))
print(await client.get_rmi("NVDA"))

print(await client.get_rmi("AAPL", "2013-01-01"))
print(await client.get_rsi("AAPL", "2013-01-01"))
```
# This tool has the ability to bruteforce valid SKUs from the 
# Star Citizen store. Why? Dunno. You can find hidden SKUs sometimes
# and if you are awaiting the release of a ship, instead of refreshing
# the webpage you can simply loop adding the ship SKU to your cart.

# To use this tool you need to fill-in the _rsi_device, Rsi-Token, and X-Rsi-Token
# from a valid session. You can find these values from the cookie while
# you're on robertsspaceindustries.com 

# importing the requests library 
import requests 
import time
results = []

# RSI APIs
api_addToCart 		= "https://robertsspaceindustries.com/api/store/addToCart"
api_updateCart 		= "https://robertsspaceindustries.com/api/store/updateCart"
api_removeFromCart 	= "https://robertsspaceindustries.com/api/store/removeFromCart"
api_clearCart 		= "https://robertsspaceindustries.com/api/store/clearCart"

# For Routing Through BurpSuite
proxies = {"http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"}

# Setup session for cookie management
s = requests.Session()

# Set current values of an active session in browser
s.cookies.set("_rsi_device", "zzzz")	  # required or web sess logout
s.cookies.set("Rsi-Token","xxxx") # same
headers = { "X-Rsi-Token":"xxxx", # same 
			"Origin": "https://robertsspaceindustries.com"}	  # may not be necessary

# Establish a benign session to set rest of cookie values
t = s.get(url = "https://robertsspaceindustries.com/pledge/extras?product_id=72")

# How many successful "add_to_carts" we've had
success = 0

# Pre-clear the cart if you added a SKU that causes your cart to error
#s.post(url = api_clearCart, headers=headers)

# Loop through SKUs
for i in range(1, 14000):
	x = str(i)
	data = {"skus":{x:"1"}} 
	r = s.post(url = api_addToCart, json = data, headers=headers)#, proxies=proxies, verify=False) 
	#print(r.request.body)
	#print(r.text)
	print i, "\t",
	
	# SKU is not for sale
	if "SKU is not for sale" in r.text:
		print "SKU is not for sale"
	
	# SKU was successfully added to our cart
	elif "\"success\":1" in r.text:
		print "SUCCESS"
		#clear the cart if we've added 10 things to it
		success += 1
		f = open("skus.txt", "a")
		f.write(str(i) + "\n")
		f.close()
		
		# Every XXX SKUs added to cart; pause to get names and/or clear cart
		if success % 1 == 0:
			print "Press ENTER to clear cart..."
			clear = raw_input()
			print "Clearing Cart...\n\n"
			removeItem = {"sku":i}
			s.post(url = api_clearCart, headers=headers)#, json = removeItem, proxies=proxies, verify=False)
			time.sleep(1)	# time for site to update
	
	# Unknown reason for failure i.e. badge missing
	# TODO: cookie value for Rsi_Site_Auth has account badges in it. 
	# Possible to fake and make badge-restricted ships available?
	else:
		print r.text
		f = open("skus_unknown.txt", "a")
		f.write(str(i) + "\t" + r.text + "\n")
		f.close()
		



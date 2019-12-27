# Star Citizen's Obscure Toolset (S.C.O.T)

## Star Brute
This tool has the ability to bruteforce valid SKUs from the 
Star Citizen store. Why? Dunno. You can find hidden SKUs sometimes
and if you are awaiting the release of a ship, instead of refreshing
the webpage you can simply loop adding the ship SKU to your cart.

To add a ship SKU to the cart repeatedly you need to modify the file. I'll
leave that up to you.

To use this tool you need to fill-in the _rsi_device, Rsi-Token, and X-Rsi-Token
from a valid session. You can find these values from the cookie while
you're on robertsspaceindustries.com You also need a valid SKU for the 
ship you want (you can find it by inspecting the page of the ship you want.) 

## Star Parse
I wrote this tool to parse the Data.p4k game file for item locations, prices, stats, etc.
I still use this tool when brand new patches come out and sites like starcitizendb.com,
gallog.co, or erkul.games haven't updated their items yet; but for the most part those sites
are the goto resources. This script is down and dirt and requires a tool called 
unp4k(https://github.com/dolkensp/unp4k).

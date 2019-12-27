# Star Citizen's Obscure Toolset (S.C.O.T)
*Use at your own risk. Do what you feel your account/Terms of Service Allows.*

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
I still use this tool when brand new patches come out and sites like https://starcitizendb.com,
https://gallog.co, or https://erkul.games haven't updated their items yet; but for the most part those sites
are the goto resources. This script is down and dirty (i.e. has a lot of errors but it gets the
job done. It also requires a tool called unp4k(https://github.com/dolkensp/unp4k).

## Star Kill
Simple batch script to kill all instances of Star Citizen, remove the shaders directory (which
is what often causes issues with the game), and restarts the client. Using this while the game
is running will often allow you to get the "Recover Instance" prompt upon logging back in.

## Star AFK
Simple python script to prevent you from going AFK in game. Will keep you logged in by pressing keys
you define in the file at random intervals.

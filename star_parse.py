# -*- coding: utf-8 -*-
import fnmatch
import os
import json
import xml.etree.ElementTree as ET
import string
import re

#.\unp4k.exe 'C:\Program Files\Roberts Space Industries\StarCitizenPTU\LIVE\Data.p4k' Data/Scripts/ShopInventories/
#.\unp4k.exe 'C:\Program Files\Roberts Space Industries\StarCitizenPTU\LIVE\Data.p4k' Data/Localization/english/global.ini
#.\unp4k.exe 'C:\Program Files\Roberts Space Industries\StarCitizenPTU\LIVE\Data.p4k' Data/Game.dcb/libs/foundry/records/ammoparams/
#.\unp4k.exe 'C:\Program Files\Roberts Space Industries\StarCitizenPTU\LIVE\Data.p4k' Data/Game.dcb/libs/foundry/records/entities/
#.\unp4k.exe 'C:\Program Files\Roberts Space Industries\StarCitizenPTU\LIVE\Data.p4k' Data/Game.dcb/libs/foundry/records/ammoparams/
#.\unp4k.exe 'C:\Program Files\Roberts Space Industries\StarCitizenPTU\LIVE\Data.p4k' Data/Game.dcb/libs/foundry/records/turbulent/

os.system("unp4k.exe \"C:/Program Files/Roberts Space Industries/StarCitizen/LIVE/Data.p4k\" Data/Scripts/ShopInventories/")
os.system("unp4k.exe \"C:/Program Files/Roberts Space Industries/StarCitizen/LIVE/Data.p4k\" Data/Localization/english/global.ini")
os.system("unp4k.exe \"C:/Program Files/Roberts Space Industries/StarCitizen/LIVE/Data.p4k\" Data/Game.dcb")
os.system("unp4k.exe \"C:/Program Files/Roberts Space Industries/StarCitizen/LIVE/Data.p4k\" Data/Objects/gameplay/mining/rocks/*.mtl")
os.system("unforge.exe Data/Game.dcb")
os.system("del \"Data/Game.*\"")

def sanitize(s):
	x = ''.join([i if ord(i) < 128 else ' ' for i in s])
	y = x.encode('ascii','ignore')
	y = y.strip()
	return y
	
def getXmlChild(xml, search):
	it = xml
	count = 0
	try:
		for i in search:
			for j in it.getchildren():	
				if j.tag == i:
					#print i
					it = j
					count += 1
	except:
		it = None
	
	if count == len(search):
		return it
	else:
		return None

		
itemShops = {}		
for root, dirnames, filenames in os.walk('Data/Scripts/ShopInventories/'):
	for filename in fnmatch.filter(filenames, '*.json'):
		h = os.path.join(root, filename)
		j = os.path.abspath(h)
		#print "\n\nLOCATION:\t%s"%filename
		
		# open JSON file and parse
		with open(j, "r") as f:
			try:
				data = json.load(f)
			except:
				continue
			data2 = json.dumps(data, indent=4)
			
			# fuckin CIG changing shop JSON templates requires a try/except now to test which one it is
			jsonIter = ""
			try:
				jsonIter = data["Inventory"]
			except:
				jsonIter = data["Collection"]
				jsonIter = jsonIter["Inventory"]
			
			
			
			# full json object			
			for j in jsonIter:
				storeMetadata = {}
				for i in j.keys():		
					if "ID" == i: #goes last
						uuid = j["ID"]["ID"][0]
						uuid = sanitize(uuid)

						if itemShops.has_key(uuid):
							temp = {}
							temp = itemShops[uuid]["Store"]
							temp.update( storeMetadata )
							itemShops[uuid]["Store"].update( temp )
						else:
							itemShops.update( {uuid: {"Store": storeMetadata} } )
						itemShops[uuid].update( {"Name": ""} )

					else:
						#print "%30s:\t"%i,j[i]
						if storeMetadata.has_key(filename.replace(".json","")):
							storeMetadata[filename.replace(".json","")].update( {i: j[i]}  )	
						else:
							storeMetadata.update( {filename.replace(".json",""): {i: j[i]} } )
							




turbulent = {}
for root, dirnames, filenames in os.walk('./Data/libs/foundry/records/turbulent'):
	
	for filename in fnmatch.filter(filenames, '*.xml'):

		h = os.path.join(root, filename)
		j = os.path.abspath(h)
		xmlFile = ET.parse(j).getroot()	
	
		if "TurbulentEntry" not in xmlFile.tag:
			#print "*** NOT A TURBULENT FILE ***","\t",filename
			continue

		uuid = 		sanitize(xmlFile.get("__ref"))
		itemClass = sanitize(xmlFile.get("itemClass"))
		if itemShops.has_key(uuid):
			itemShops[uuid].update( {"Name": itemClass} )


# PUT ALL NAME MAPPINGS INTO A DICT
names = {}
with open("./Data/Localization/english/global.ini", "r") as f:
	for line in f:
		x = line.split("=")
		names.update( {x[0]: x[1]} )
	
#print "="*60
#print "%40s\t%10s\t%10s"%("GUNS/AMMO DAMAGE VALUES","SPEED","DAMAGE")
#print "="*60	
# RETRIEVE AMMO PARAMATERS IN THE FORM OF { UUID: [metadata] }		
ammoParams = {}			
for root, dirnames, filenames in os.walk('./Data/libs/foundry/records/ammoparams'):
	
	for filename in fnmatch.filter(filenames, '*.xml'):

		h = os.path.join(root, filename)
		j = os.path.abspath(h)
		xmlFile = ET.parse(j).getroot()

		ammoMeta = {}
		
		try:
			uuid  = sanitize(xmlFile.get("__ref"))
			speed = float(xmlFile.get("speed"))
			try:
				size = filename.split("_")[2]
				if len(size) > 2:
					size = 0
			except:
				size = 0
			dist = float(float(xmlFile.get("lifetime")) * float(speed))
			ammoMeta.update( {"Speed": speed } )
			ammoMeta.update( {"Size": size} )
			ammoMeta.update( {"Distance": dist} )
		except:
			#print "*** NOT AN AMMO PARAM FILE ***"
			continue
		explosive = ["projectileParams", "BulletProjectileParams", "detonationParams", "ProjectileDetonationParams", "explosionParams", "damage", "DamageInfo"]
		banu = [ "projectileParams", "TachyonProjectileParams", "damage", "DamageParams" ]
		bullet =["projectileParams", "BulletProjectileParams", "damage", "DamageInfo"]

		#print xmlFile.tag
		# ORDER MATTERS HERE. Explosive will be seen higher in the file, then banu, then bullet I think
		retrieve = getXmlChild(xmlFile, explosive)
		if retrieve == None:
			#print "EXPLOSIVE NOT FOUND"
			retrieve = getXmlChild(xmlFile, banu)
			if retrieve == None:
				#print "BANU NOT FOUND"
				retrieve = getXmlChild(xmlFile, bullet)
				if retrieve == None:
					#print "NO AMMO PARAMATERS FOUND"
					#raw_input()
					continue
		for x in retrieve.attrib:
			try:
				ammoMeta.update( {x: float(retrieve.get(x)) } )
				#print "%20s\t%d"%(x,int(retrieve.get(x)))
			except:
				error = 1		
		ammoParams.update( {uuid: ammoMeta} )


# RETRIEVE ALL ENTITIES  IN THE FORM { EntityClassDefinition: { englishName, other metadata } }
entities = {}			
for root, dirnames, filenames in os.walk('./Data/libs/foundry/records/entities'):
	
	for filename in fnmatch.filter(filenames, '*.xml'):

		h = os.path.join(root, filename)
		j = os.path.abspath(h)
		xmlFile = ET.parse(j).getroot()		
		
		if "EntityClassDefinition" not in xmlFile.tag:
			#print "*** NOT AN ENTITY FILE ***","\t",filename
			continue
			
		entityUUID	= sanitize(xmlFile.get("__ref"))
		
		if not itemShops.has_key(entityUUID):
			#print "shops don't sell %s"% sanitize(xmlFile.tag.replace("EntityClassDefinition.",""))
			continue

		entityClass = sanitize(xmlFile.tag.replace("EntityClassDefinition.",""))	

		localizationPaths =[["Components", "SCItemPurchasableParams", "AttachDef", "Localization"],
							["Components", "SAttachableComponentParams", "AttachDef", "Localization"],
							["Components", "SCItemPurchasableParams"],
							["Components", "CommodityComponentParams"]]
		localizationName=[ "displayName", "Name", "name"]
		localizationDesc=[ "Description", "description"]
		
		localization = ""
		itemName = ""
		itemDesc = ""
		for path in localizationPaths:
			localization = getXmlChild(xmlFile, path)
			
			if localization == None:
				continue
			else:
				for name in localizationName:
					try:
						itemName = sanitize(localization.get(name)).replace("@","")
						if "item" not in itemName:
							itemName = "None"
					except:
						continue
						
				for desc in localizationDesc:
					try:
						itemDesc = sanitize(localization.get(desc)).replace("@","")
					except:
						continue			
		
		if names.has_key(itemName):
			itemShops[entityUUID].update( {"Name": sanitize(names[itemName]) } )
		#sometimes there is a @Loc_Placeholder instead of an actual name, so if the name isn't found, use the descriptive entityclass name	
		else:
			itemShops[entityUUID].update( {"Name": sanitize(xmlFile.tag.replace("EntityClassDefinition." ,"")) } )
				
		if names.has_key(itemDesc):
			itemShops[entityUUID].update( {"Description": sanitize(names[itemDesc]) } )
		
		
		
		
		itemShops[entityUUID].update( {"Class": entityClass} )
		
		
		# Retrieve metadata for power, shield, quantum drive, or cooler.
		testComponentType = entityClass.lower().split("_")[0]
		
		if testComponentType == "qdrv":	
			quantumPath =["Components", "SCItemQuantumDriveParams", "params"]
			q = getXmlChild(xmlFile, quantumPath)
			qspeed = q.get("driveSpeed")
			qspeed = int(float(qspeed))
			size = entityClass.split("_")[2]
			itemShops[entityUUID].update( {"QSpeed": qspeed} )
			itemShops[entityUUID].update( {"Size": size} )

		elif testComponentType == "cool":
			coolPath =["Components", "SCItemCoolerParams"]
			q = getXmlChild(xmlFile, coolPath)
			cooling = q.get("CoolingRate")
			cooling = int(float(cooling))
			size = entityClass.split("_")[2]
			itemShops[entityUUID].update( {"Cooling": cooling} )
			itemShops[entityUUID].update( {"Size": size} )

		elif testComponentType =="shld":
			shieldPath =["Components", "SCItemShieldGeneratorParams"]
			q = getXmlChild(xmlFile, shieldPath)
			health = q.get("MaxShieldHealth")
			health = int(float(health))
			size = entityClass.split("_")[2]
			itemShops[entityUUID].update( {"Health": health} )
			itemShops[entityUUID].update( {"Size": size} )

		elif testComponentType == "powr":
			powerPath =["Components", "EntityComponentPowerConnection"]
			q = getXmlChild(xmlFile, powerPath)
			power = q.get("PowerDraw")
			power = int(float(power))
			size = entityClass.split("_")[2]
			itemShops[entityUUID].update( {"Power": power} )
			itemShops[entityUUID].update( {"Size": size} )



		# If an ammoParam record is found, then retrieve the weapon metadata
		ammoParamsRecord  = getXmlChild(xmlFile, ["Components", "SAmmoContainerComponentParams"])
		if ammoParamsRecord != None:
			ammoUUID = sanitize(ammoParamsRecord.get("ammoParamsRecord"))
			dmg = 0
			speed = 0
			size = 0
			dist = 0
			if ammoParams.has_key(ammoUUID):
				itemShops[entityUUID].update( {"Size": 0} )
				itemShops[entityUUID].update( {"Damage": 0} )
				itemShops[entityUUID].update( {"Speed": 0} )
				itemShops[entityUUID].update( {"Distance": 0} )
				
				for a in ammoParams[ammoUUID]:
					if "speed" in a.lower():
						speed = ammoParams[ammoUUID][a]
					elif "damage" in a.lower():
						dmg += float(ammoParams[ammoUUID][a])	
					elif "distance" in a.lower():
						dist = ammoParams[ammoUUID][a]
					elif "size" in a.lower():
						size = ammoParams[ammoUUID][a]

				itemShops[entityUUID].update( {"Size": size} )
				itemShops[entityUUID].update( {"Damage": dmg} )
				itemShops[entityUUID].update( {"Speed": speed} )				
				itemShops[entityUUID].update( {"Distance": dist} )


# Extract components and weapons			
weps = []
qdrv = []
cool = []
shld = []
powr = []	
for x in itemShops:
	if itemShops[x].has_key("Speed") and itemShops[x].has_key("Damage"):
		if float(itemShops[x]["Damage"]) > 0:
			weps.append( [ itemShops[x]["Name"], itemShops[x]["Size"], int(itemShops[x]["Damage"]), int(itemShops[x]["Speed"]), int(itemShops[x]["Distance"])] )
			
	elif itemShops[x].has_key("QSpeed"):
		qdrv.append( [itemShops[x]["Name"], itemShops[x]["Size"], itemShops[x]["QSpeed"] ] )
		
	elif itemShops[x].has_key("Cooling"):
		cool.append( [itemShops[x]["Name"], itemShops[x]["Size"], itemShops[x]["Cooling"] ] )
	
	elif itemShops[x].has_key("Health"):
		shld.append( [itemShops[x]["Name"], itemShops[x]["Size"], itemShops[x]["Health"] ] )
		
	elif itemShops[x].has_key("Power"):
		powr.append( [itemShops[x]["Name"], itemShops[x]["Size"], itemShops[x]["Power"] ] )
			

import operator

# output weapon table
s = sorted(weps, key = operator.itemgetter(1, 2))
print "%-40s\t%-10s\t%-10s\t%-10s\t%-10s"%("WEAPON","SIZE","DAMAGE","M/S","DISTANCE")
print "="*88	
for x in s:
	print "%-40s\t%-10s\t%-10s\t%-10s\t%-10s"%(x[0], x[1], x[2], x[3], x[4])

	
# output shield table 
s = sorted(shld, key = operator.itemgetter(1, 2))
print "\n\n%-40s\t%-10s\t%-10s"%("SHIELD","SIZE","HEALTH")
print "="*88	
for x in s:
	print "%-40s\t%-10s\t%-10s"%(x[0], x[1], x[2])
	
# output cooler table 
s = sorted(cool, key = operator.itemgetter(1, 2))
print "\n\n%-40s\t%-10s\t%-10s"%("COOLER","SIZE","COOLING")
print "="*88	
for x in s:
	print "%-40s\t%-10s\t%-10s"%(x[0], x[1], x[2])
	
# output power table 
s = sorted(powr, key = operator.itemgetter(1, 2))
print "\n\n%-40s\t%-10s\t%-10s"%("POWERPLANT","SIZE","POWER")
print "="*88	
for x in s:
	print "%-40s\t%-10s\t%-10s"%(x[0], x[1], x[2])
	
# output quantum table 
s = sorted(qdrv, key = operator.itemgetter(1, 2))
print "\n\n%-40s\t%-10s\t%-10s"%("QUANTUMDRIVE","SIZE","SPEED")
print "="*88	
for x in s:
	print "%-40s\t%-10s\t%-10s"%(x[0], x[1], x[2])
	

# current list of vice commodities you can buy 
print "\n\n%-40s"%("VICE COMMODITIES")
print "="*88
for root, dirnames, filenames in os.walk('./Data/libs/foundry/records/entities/commodities/vice'):
	for filename in fnmatch.filter(filenames, '*.xml'):
		print filename.split(".")[0]

	
# print out current known drug labs (permanent ones, not dynamically generated for missions)
print "\n\n%-40s\t%-10s"%("DRUG LABS (NOT DYNAMIC MISSION DRUG LABS)","LOCATION")
print "="*88		
for x in names:
	if "_desc" not in x.lower():
		if "druglab" in x.lower():
			print "%-40s\t%s"%(names[x].strip(),names[x.split("_")[0]].strip())
		elif "stash" in x.lower():
			if "stash" == x.lower().split("_")[1]:
				print "%-40s\t%s"%(names[x].strip(),names[x.split("_")[0]].strip())

		
# print out the mineable rocks and which planets they can be found on	
# TODO: the mining rocks data has percentages of composite materials. those materials
# can be correlated to the 	Game.dcb/libs/foundry/records/mining/mineableelements __ref ID.
print "\n\n%-40s\t%-10s"%("ROCK NAME","PLANET")
print "="*88	
for root, dirnames, filenames in os.walk('./Data/Objects/gameplay/mining/rocks'):	
	for filename in fnmatch.filter(filenames, '*.mtl'):	
		if "mining_rock" in filename:
			a = filename.split("_")
			planet = a[3].split(".")[0]
			aa = ("hud_%s_%s_name_%s"%(a[0],a[1],a[2])).replace("0","")
			rockName = names[aa].strip()
			print "%-40s\t%s"%(rockName,planet)
			
	
# print details of items	
for x in itemShops:
	print "\n"
	try:
		name = itemShops[x]["Name"]
	except:
		name = "None"
	
	try:
		nClass = itemShops[x]["Class"]
	except:
		nClass = "None"

	print "%-8s:\t%s"%("UUID",x)
	print "%-8s:\t%s"%("NAME",name)
	print "%-8s:\t%s"%("CLASS",nClass)

	
	if itemShops[x].has_key("Damage"):
		if int(itemShops[x]["Damage"]) > 0:
			print "%-8s:\t%s"%("SIZE",itemShops[x]["Size"])
			print "%-8s:\t%s"%("DAMAGE",itemShops[x]["Damage"])
			print "%-8s:\t%s"%("SPEED", itemShops[x]["Speed"])
			print "%-8s:\t%s"%("DIST",itemShops[x]["Distance"])

			
	elif itemShops[x].has_key("QSpeed"):
		print "%-8s:\t%s"%("SIZE",itemShops[x]["Size"])
		print "%-8s:\t%s"%("QSPEED",itemShops[x]["QSpeed"])
		
	elif itemShops[x].has_key("Cooling"):
		print "%-8s:\t%s"%("SIZE",itemShops[x]["Size"])
		print "%-8s:\t%s"%("COOLING",itemShops[x]["Cooling"])
	
	elif itemShops[x].has_key("Health"):
		print "%-8s:\t%s"%("SIZE",itemShops[x]["Size"])
		print "%-8s:\t%s"%("SHIELD",itemShops[x]["Health"])
		
	elif itemShops[x].has_key("Power"):
		print "%-8s:\t%s"%("SIZE",itemShops[x]["Size"])
		print "%-8s:\t%s"%("POWER",itemShops[x]["Power"])

		
	if itemShops[x].has_key("Description"):
		print "%-8s:\t%-50s"%("DESCRIP",itemShops[x]["Description"].strip().replace("\\n","\\n\\t\\t\\t").replace("\\n\\t\\t\\t\\n\\t\\t\\t","\\n\\t\\t\\t").decode('string_escape'))
	else:
		print "%-8s:\t%s"%("DESC","None")
	
	for i in itemShops[x]["Store"]:
		print "%-8s:\t%s"%("STORE",i)
		for h in itemShops[x]["Store"][i]:
			print "\t\t\t\t%-20s:\t\t%s"%(h, itemShops[x]["Store"][i][h])

quit()


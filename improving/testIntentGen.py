from intentGen import IntentGen
import json


with open('intent2.json', 'r') as file : data = json.load(file)
intentGen = IntentGen(data)
intentGen.gen()
intentGen.write_on_intent("intent4")
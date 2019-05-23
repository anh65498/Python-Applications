# Anh Pham and Omar
# An application that lets the user look up US national parks within a state
# so that they can plan their summer vacation trips.


import requests, json

BaseURL = "https://developer.nps.gov/api/v1"
APIkeys = "Dd2O3pfwKcMrRVm2TQP4tvlGGbNffyYriLglLPdh"

# look up state code using states_hash.json
with open('states_hash.json', 'r') as fh:
    state_dict = json.load(fh)

state_name = input("Enter a state's name you want to look up: ")
for k, v in state_dict.items():
    if v == state_name:
        state_code = k
    # what if there's no match?????

URL     = BaseURL + "/parks?stateCode={0}&api_key={1}".format(state_code, APIkeys)


page = requests.get(URL)
resultDict = page.json()
print(resultDict, end="\n\n")

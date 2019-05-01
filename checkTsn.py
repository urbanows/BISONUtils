#import urllib.request
#import urllib.parse
import json

#url = 'https://data.usgs.gov/solr/occurrences/select/?q=-centroid:[%22%22%20TO%20*]%20AND%20year:[2015%20TO%202017]&fq=geo:%22IsWithin(POLYGON%20((-80.388686269521713%2025.182016849517822,%20-80.498195916414261%2025.760813742876053,%20-81.405306428670883%2025.889948308467865,%20-81.455898761749268%2025.889483511447906,%20-81.5180467069149%2025.831523925065994,%20-81.518311768770218%2025.82014736533165,%20-81.204896301031113%2025.226881086826324,%20-81.161738961935043%2025.156834214925766,%20-81.02135905623436%2025.00069060921669,%20-80.937817871570587%2024.912669092416763,%20-80.887194097042084%2024.871733695268631,%20-80.835251480340958%2024.849981546401978,%20-80.734941810369492%2024.897992581129074,%20-80.570307523012161%2024.993271291255951,%20-80.51714026927948%2025.027157038450241,%20-80.4227964580059%2025.126799374818802,%20-80.389390289783478%2025.18007093667984,%20-80.388686269521713%2025.182016849517822)))%20distErrPct=0.1%22&start=0&rows=0&wt=json&facet=true&facet.limit=-1&facet.mincount=1&facet.pivot=kingdom,scientificName&indent=true'\n",
#f = urllib.request.urlopen(url)
fC=open("chsTsn.json","r")
jsonResultsC=json.loads(fC.read().decode('utf-8'))

facetsC=jsonResultsC['facet_counts']['facet_fields']['ITIStsn']
print(len(facetsC))


fG=open("chsTsn.json","r")
jsonResultsG=json.loads(fG.read().decode('utf-8'))

facetsG=jsonResultsG['facet_counts']['facet_fields']['ITIStsn']
print(len(facetsG))


for index, item in enumerate(facets):
    print("Kingdom:", item["value"], "Count:",item["count"])
    print("----")

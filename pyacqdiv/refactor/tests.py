import metadata
import parsers

cfg = parsers.CorpusConfigParser()

print("RUSSIAN:")
cfg.read("Russian.ini")
imdi = metadata.Imdi(cfg, "../../corpora/Russian/metadata/IMDI/A00210817.imdi")
for k, v in imdi.metadata.items():
    print(k, v)
    print()
# print(imdi.metadata['session']['location']['address'])
print("#####################")

print("CREE;")
cfg.read("Cree.ini")
xml = metadata.Chat(cfg, "../../corpora/Cree/xml/Ani/2005-09-14.xml")
for k, v in xml.metadata.items():
    print(k, v)
    print()
print("#####################")

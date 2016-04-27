# Japanese CHILDES
# xmllint --noout --schema talkbank.xsd aprm19990515.xml

# Russian
xmllint --noout --schema IMDI_3.0.xsd A09231013.imdi
# Passes:
xmllint --noout --schema IMDI_3.0.xsd V10840108.imdi

# Check without xsd
xmllint --noout A09231013.imdi
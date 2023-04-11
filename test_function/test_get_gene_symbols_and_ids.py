import pandas as pd
from biomart import BiomartServer
ensg_ids = ['ENSG00000157764', 'ENSG00000198242']

# Query Biomart for gene symbols and IDs
server = BiomartServer("http://www.ensembl.org/biomart")
ensembl = server.datasets['hsapiens_gene_ensembl']
response = ensembl.search({
    'attributes': ['ensembl_gene_id', 'external_gene_name', 'entrezgene_id'],
    'filters': {'ensembl_gene_id': ensg_ids}
})

# Create dictionaries to map ENSG IDs to gene symbols and gene IDs
ensg_to_symbol = {}
ensg_to_id = {}
for row in response.iter_lines():
    row = row.decode('utf-8')
    ensg, symbol, gene_id = row.split('\t')
    ensg_to_symbol[ensg] = symbol
    ensg_to_id[symbol] = gene_id


print(ensg_to_symbol)
print(ensg_to_id)
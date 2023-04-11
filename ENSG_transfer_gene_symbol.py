import pandas as pd
from biomart import BiomartServer
from tqdm import tqdm
import re

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def convert_ensembl_to_gene_symbols(input_file, output_file, chunk_size=50):
    df = pd.read_excel(input_file, header=0, index_col=0)
    # Remove decimals from Ensembl IDs only
    # df.index = df.index.map(lambda x: x.split('.')[0] if re.match('^ENSG', x) else x)
    df.index = df.index.map(lambda x: str(x).split('.')[0] if re.match('^ENSG', str(x)) else x)
    #
    ensg_ids = df.index.tolist()

    server = BiomartServer("http://www.ensembl.org/biomart")
    ensembl = server.datasets['hsapiens_gene_ensembl']

    ensg_to_symbol = {}
    ensg_to_id = {}
    for ensg_chunk in tqdm(list(chunks(ensg_ids, chunk_size)), desc="Processing chunks"):
        # Check if the IDs in the chunk are Ensembl or Entrez IDs
        id_type = 'ensembl_gene_id' if re.match('^ENSG', str(ensg_chunk[0])) else 'entrezgene_id'

        response = ensembl.search({
            'attributes': ['ensembl_gene_id', 'external_gene_name', 'entrezgene_id'],
            'filters': {id_type: ensg_chunk}
        })
        if id_type=='ensembl_gene_id':
            print(f'id is {id_type}')
            for row in response.iter_lines():
                row = row.decode('utf-8')
                values = row.split('\t')
                if len(values) == 3:
                    ensg, symbol, gene_id = values
                    ensg_to_symbol[ensg] = symbol
                    ensg_to_id[symbol] = gene_id
                else:
                    print(f"Warning: Skipping row with unexpected values: {row}")
        else:
            print(f'id is {id_type}')
            for row in response.iter_lines():
                row = row.decode('utf-8')
                values = row.split('\t')
                if len(values) == 3:
                    ensg, symbol, gene_id = values
                    ensg_to_symbol[gene_id] = symbol
                    # ensg_to_id[symbol] = gene_id
                else:
                    print(f"Warning: Skipping row with unexpected values: {row}")



    df.index = df.index.to_series().map(ensg_to_symbol)
    # df['gene_id'] = df.index.to_series().map(ensg_to_id)
    print(df.index)
    df.to_excel(output_file)



#
if __name__=='__main__':
    input_file = 'data_source/GSE91061_fpkm.xlsx'
    output_file = 'generated_data/GSE91061_fpkm_transfer.xlsx'
    convert_ensembl_to_gene_symbols(input_file, output_file)
    print('convert finished')

import pandas as pd
# df=pd.read_excel('GSE135222.xlsx',index_col=0)
# print(df)

import os
import pandas as pd

def read_gene_list_from_file(gene_list_file):
    gene_list_df = pd.read_excel(gene_list_file)
    return gene_list_df.iloc[:, 0].tolist()
def read_gene_lists_from_directory(directory):
    gene_lists = {}

    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(directory, filename)
            gene_list = read_gene_list_from_file(file_path)
            # Use the filename without the extension as the key
            key = os.path.splitext(filename)[0]
            gene_lists[key] = gene_list

    return gene_lists
def filter_genes_by_name(df, gene_list):
    # Filter the DataFrame based on the given gene list
    filtered_genes = []
    for gene in gene_list:
        if gene in df.index:
            filtered_genes.append(gene)
        else:
            print(f"This gene {gene} is not in the index, we have ignored it.")
    filtered_df = df.loc[filtered_genes]
    return filtered_df
def process_and_save_gene_lists(data_excel, gene_lists, output_directory):
    # Read the Excel file into a pandas DataFrame with the first column as the index
    df = pd.read_excel(data_excel, index_col=0)

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for key, gene_list in gene_lists.items():
        filtered_df = filter_genes_by_name(df, gene_list)
        output_file = os.path.join(output_directory, f"{key}.xlsx")
        filtered_df.to_excel(output_file)
        print(f"Filtered data for '{key}' saved to {output_file}")
if __name__ == "__main__":
    gene_list_directory = "data_source"
    source_data_excel = "GSE135222.xlsx"
    output_dir="generated_data"
    gene_lists = read_gene_lists_from_directory(gene_list_directory)
    process_and_save_gene_lists(source_data_excel, gene_lists, output_dir)
    # print(gene_lists)

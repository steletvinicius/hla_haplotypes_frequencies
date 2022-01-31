import pandas as pd
import glob
import streamlit as st

choice_hap_or_al    =   {
    # 'Choose an option':'empty',
    'ALLELE frequency': 'allele',
    'HAPLOTYPE frequency': 'haplotype' 
    }

choice_fam_or_unr   =   {
    # 'Choose an option':'empty',
    'Families': 'family',
    'Unrelated individuais': 'unrelated'
    }

alleles =   {
    'HLA-A': 'Global_HLA-A_Locus_Summary_2018-08-01.xlsx',
    'HLA-C': 'Global_HLA-C_Locus_Summary_2018-08-01.xlsx',
    'HLA-B': 'Global_HLA-B_Locus_Summary_2018-08-01.xlsx',
    'HLA-DRB3': 'Global_HLA-DRB3_Locus_Summary_2018-07-31.xlsx',
    'HLA-DRB4': 'Global_HLA-DRB4_Locus_Summary_2018-07-31.xlsx',
    'HLA-DRB5': 'Global_HLA-DRB5_Locus_Summary_2018-07-31.xlsx',
    'HLA-DRB1': 'Global_HLA-DRB1_Locus_Summary_2018-08-01.xlsx',
    'HLA-DQA1': 'Global_HLA-DQA1_Locus_Summary_2018-07-31.xlsx',
    'HLA-DQB1': 'Global_HLA-DQB1_Locus_Summary_2018-08-01.xlsx',
    'HLA-DPA1': 'Global_HLA-DPA1_Locus_Summary_2018-07-31.xlsx',
    'HLA-DPB1': 'Global_HLA-DPB1_Locus_Summary_2018-08-01.xlsx',
}

family_haplotypes = {
    "A~C~B":                                    'Global_ACB_Haplotype_Summary_2018-08-01.xlsx',
    "A~C~B~DRB1~DQB1":                          'Global_ACBDRB1DQB1_Haplotype_Summary_2018-08-01.xlsx',
    "A~C~B~DRB3/4/5-DRB1~DQA1~DQB1":            'Global_ACBDRDQ_Haplotype_Summary_2018-07-31.xlsx',
    "C~B":                                      'Global_CB_Haplotype_Summary_2018-08-01.xlsx',
    "C~B~DRB1~DQB1":                            'Global_CBDRB1DQB1_Haplotype_Summary_2018-08-01.xlsx',
    "C~B-DRB3/4/5~DRB1~DQA1~DQB1":              'Global_CBDRDQ_Haplotype_Summary_2018-07-31.xlsx',
    'C~B-DRB3/4/5~DRB1~DQA1~DQB1~DPA1~DPB1':    'Global_CBDRDQDP_Haplotype_Summary_2018-07-31.xlsx',
    "DPA1~DPB1":                                'Global_DP_Haplotype_Summary_2018-07-31.xlsx',
    "DQA1~DQB1":                                'Global_DQ_Haplotype_Summary_2018-07-31.xlsx',
    'DRB3/4/5~DRB1':                            'Global_DR_Haplotype_Summary_2018-07-31.xlsx',
    "DRB1~DQB1":                                'Global_DRB1DQB1_Haplotype_Summary_2018-08-01.xlsx',
    'DRB3/4/5~DRB1~DQA1~DQB1':                  'Global_DRDQ_Haplotype_Summary_2018-07-31.xlsx',
    'DRB3/4/5~DRB1~DQA1~DQB1~DPA1~DPB1':        'Global_DRDQDP_Haplotype_Summary_2018-07-31.xlsx',
    'A~C~B-DRB3/4/5-DRB1~DQA1~DQB1~DPA1~DPB1':  'Global_Full_Haplotype_Summary_2018-08-01.xlsx'
}

unrelated_haplotypes = {
    'A~B':                                  'Table2_Unrelated_AB_haplotype_final_081318.xlsx',
    'A~C':                                  'Table3_Unrelated_AC_haplotype_final_081318.xlsx',
    'C~B':                                  'Table4_Unrelated_CB_haplotype_final_081318.xlsx',
    'DQA1~DQB1':                            'Table5_Unrelated_DQA1DQB1_haplotype_final_081318.xlsx',
    'DRB1~DQA1':                            'Table6_Unrelated_DRB1DQA1_haplotype_final_081318.xlsx',
    'DRB1~DQB1':                            'Table7_Unrelated_DRB1DQB1_haplotype_final_081318.xlsx',
    'DPA1~DPB1':                            'Table8_Unrelated_DPA1DPB1_haplotype_final_081318.xlsx',
    'A~C~B-DRB1~DQB1':                      'Table9_Unrelated_ACBDRB1DQB1_haplotype_final_081318.xlsx',
    'A~C~B-DRB3/4/5-DRB1~DQB1':             'Table10_Unrelated_ACBDRB345DRB1DQB1_haplotype_final_081318.xlsx',
    'A~C~B-DRB3/4/5-DRB1~DQA1~DQB1':        'Table11_Unrelated_ACBDRB3/45DRB1DQA1DQB1_haplotype_final_081318.xlsx',
    'DRB3/4/5-DRB1~DQA1~DQB1':              'Table12_Unrelated_DRB345DRB1DQA1DQB1_haplotype_final_081318.xlsx',
    'A~C~B-DRB1~DQB1~DPB1':                 'Table13_Unrelated_ACBDRB1DQB1DPB1_haplotype_final_081318.xlsx',
    'A~C~B-DRB3/4/5-DRB1~DQA1~DQB1~DPA1~DPB1': 'Table14_Unrelated_ACBDRB345DRB1DQA1DQB1DPA1DPB1_haplotype_final_081318.xlsx',
}
path_family_data    =   './17th-IHIW-Family-Studies-Data/'
path_unrelated_data =   './17th-IHIW-Unrelated-Studies-Data/'
allele_frequencies_unr  =   'Table1_Unrelated_1_locus_allele_final_0081318.xlsx'

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def family_file_name(hap_or_allele, hla_query):
    if hap_or_allele == 'allele':
        table = alleles[hla_query] 
    else:
        table   =   family_haplotypes[hla_query]
    path_file   =   path_family_data + table
    df   =   pd.read_excel(path_file, header=[3,4,5])
    return df


def unrelated_file_name(hap_or_allele, hla_query):
    if hap_or_allele == 'haplotype':
        table       =   unrelated_haplotypes[hla_query]
        path_file   =   path_unrelated_data + table
        df          =   pd.read_excel(
            path_file,
            header=[1]
            )
    else:
        table       =   allele_frequencies_unr
        path_file   =   path_unrelated_data + table
        df          =   pd.read_excel(
            path_file,
            sheet_name = hla_query[4:],
            header=[1]
            )
    return df


def table_search(hap_or_allele, fam_or_unr, hla_query ):
    if fam_or_unr == 'family':
        df   =   family_file_name(hap_or_allele, hla_query)
    else:
        df   =   unrelated_file_name(hap_or_allele, hla_query)

    # df   =   pd.read_excel(path_file, header=[3,4,5])
    return df


# Choose between haplotype or individual allele frequency
answer_one  = st.sidebar.radio(
    'Choose what kind of data you are looking for :',
    choice_hap_or_al.keys(),
    key='hap_allele'
    )

# Choose between family or unrelated
answer_two  = st.sidebar.radio(
    'Choose the data source :',
    choice_fam_or_unr.keys(),
    key='fam_unr'
    )

# disabled = False if choice_hap_or_al[answer_one] == 'allele' else True


if choice_hap_or_al[answer_one]   ==  'allele':
    # Choose which HLA gene
    hla_query  = st.sidebar.selectbox(
        'Choose the HLA gene :',
        alleles,
        key='hla_allele',
        # disabled= disabled
        )
else:
    if choice_fam_or_unr[answer_two] == 'family':
        hla_query  = st.sidebar.selectbox(
            'Choose the HLA haplotype :',
            family_haplotypes.keys(),
            key='hla_allele',
            # disabled= disabled
            )
    else:
        hla_query  = st.sidebar.selectbox(
            'Choose the HLA haplotype :',
            unrelated_haplotypes.keys(),
            key='hla_allele',
            # disabled= disabled
            )

button  =   st.sidebar.button('Search')

if button:
    # if choice_fam_or_unr[answer_two] == 'family':
    dataframe = table_search(
        choice_hap_or_al[answer_one],
        choice_fam_or_unr[answer_two],
        hla_query
        )
# with st.container():
    # st.dataframe(dataframe.style.highlight_max(axis=0), 2000, 1000)
    st.table(dataframe)


    csv = convert_df(dataframe)

    st.download_button(
        label="Download this table data as CSV",
        data=csv,
        file_name='table.csv',
        mime='text/csv',
    )
    


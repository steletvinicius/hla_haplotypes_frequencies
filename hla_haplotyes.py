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
    'Unrelated individuals': 'unrelated'
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
    "A~C~B~DRB345~DRB1~DQA1~DQB1":            'Global_ACBDRDQ_Haplotype_Summary_2018-07-31.xlsx',
    "C~B":                                      'Global_CB_Haplotype_Summary_2018-08-01.xlsx',
    "C~B~DRB1~DQB1":                            'Global_CBDRB1DQB1_Haplotype_Summary_2018-08-01.xlsx',
    "C~B~DRB345~DRB1~DQA1~DQB1":              'Global_CBDRDQ_Haplotype_Summary_2018-07-31.xlsx',
    'C~B~DRB345~DRB1~DQA1~DQB1~DPA1~DPB1':    'Global_CBDRDQDP_Haplotype_Summary_2018-07-31.xlsx',
    "DPA1~DPB1":                                'Global_DP_Haplotype_Summary_2018-07-31.xlsx',
    "DQA1~DQB1":                                'Global_DQ_Haplotype_Summary_2018-07-31.xlsx',
    'DRB345~DRB1':                            'Global_DR_Haplotype_Summary_2018-07-31.xlsx',
    "DRB1~DQB1":                                'Global_DRB1DQB1_Haplotype_Summary_2018-08-01.xlsx',
    'DRB345~DRB1~DQA1~DQB1':                  'Global_DRDQ_Haplotype_Summary_2018-07-31.xlsx',
    'DRB345~DRB1~DQA1~DQB1~DPA1~DPB1':        'Global_DRDQDP_Haplotype_Summary_2018-07-31.xlsx',
    'A~C~B~DRB345~DRB1~DQA1~DQB1~DPA1~DPB1':  'Global_Full_Haplotype_Summary_2018-08-01.xlsx'
}

unrelated_haplotypes = {
    'A~B':                                  'Table2_Unrelated_AB_haplotype_final_081318.xlsx',
    'A~C':                                  'Table3_Unrelated_AC_haplotype_final_081318.xlsx',
    'C~B':                                  'Table4_Unrelated_CB_haplotype_final_081318.xlsx',
    'DQA1~DQB1':                            'Table5_Unrelated_DQA1DQB1_haplotype_final_081318.xlsx',
    'DRB1~DQA1':                            'Table6_Unrelated_DRB1DQA1_haplotype_final_081318.xlsx',
    'DRB1~DQB1':                            'Table7_Unrelated_DRB1DQB1_haplotype_final_081318.xlsx',
    'DPA1~DPB1':                            'Table8_Unrelated_DPA1DPB1_haplotype_final_081318.xlsx',
    'A~C~B~DRB1~DQB1':                      'Table9_Unrelated_ACBDRB1DQB1_haplotype_final_081318.xlsx',
    'A~C~B~DRB345~DRB1~DQB1':             'Table10_Unrelated_ACBDRB345DRB1DQB1_haplotype_final_081318.xlsx',
    'A~C~B~DRB345~DRB1~DQA1~DQB1':        'Table11_Unrelated_ACBDRB345DRB1DQA1DQB1_haplotype_final_081318.xlsx',
    'DRB345~DRB1~DQA1~DQB1':              'Table12_Unrelated_DRB345DRB1DQA1DQB1_haplotype_final_081318.xlsx',
    'A~C~B~DRB1~DQB1~DPB1':                 'Table13_Unrelated_ACBDRB1DQB1DPB1_haplotype_final_081318.xlsx',
    'A~C~B~DRB345~DRB1~DQA1~DQB1~DPA1~DPB1': 'Table14_Unrelated_ACBDRB345DRB1DQA1DQB1DPA1DPB1_haplotype_final_081318.xlsx',
}
path_family_data    =   './17th-IHIW-Family-Studies-Data/'
path_unrelated_data =   './17th-IHIW-Unrelated-Studies-Data/'
allele_frequencies_unr  =   'Table1_Unrelated_1_locus_allele_final_0081318.xlsx'

# @st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep=';').encode('utf-8')


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


def table_filter(dataframe, args_list):
    col =   dataframe.columns[0]
    return dataframe.loc[dataframe[col].isin(args_list)]



st.set_page_config(
    page_title="HLA frequency data explorer - 17th HLA Workshop",
    # page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

with st.sidebar:
    # with st.form('form_one'):
    st.title('HLA frequency haplotype data explorer ')
    st.subheader('Step 1. Choose among single HLA allele or haplotype frequency:')
    # Choose between haplotype or individual allele frequency
    answer_one  = st.radio(
        'single HLA allele or Haplotype frequency',
        choice_hap_or_al.keys(),
        key='hap_allele'
        )
    st.subheader('Step 2. Choose the data source:')
    # Choose between family or unrelated
    answer_two  = st.radio(
        'Data from families or unrelated individuals',
        choice_fam_or_unr.keys(),
        key='fam_unr'
        )

    if choice_hap_or_al[answer_one]   ==  'allele':
        # Choose which HLA gene
        st.subheader('Step 3. Choose the HLA gene:')
        hla_query  = st.selectbox(
            'Choose the HLA gene :',
            alleles,
            key='hla_allele',
            # disabled= disabled
            )
    else:
        st.subheader('Step 3. Choose the HLA Haplotype:')
        if choice_fam_or_unr[answer_two] == 'family':
            hla_query  = st.selectbox(
                'Choose the HLA haplotype :',
                family_haplotypes.keys(),
                key='hla_allele',
                # disabled= disabled
                )
        else:
            hla_query  = st.selectbox(
                'Choose the HLA haplotype :',
                unrelated_haplotypes.keys(),
                key='hla_allele',
                # disabled= disabled
                )
    dataframe   =   table_search(
        choice_hap_or_al[answer_one],
        choice_fam_or_unr[answer_two],
        hla_query
        )

    if choice_hap_or_al[answer_one]   ==  'allele':
        form_two_list    =   sorted(dataframe.iloc[:,0].unique())
        label_two        =   'Step 4. Filter by HLA allele:'
        st.subheader(label_two)
        alleles_chosen  = st.multiselect(
            'Choose the HLA allele',
            form_two_list,
            key='options_form_two'
            )
    else:
        label_two        =   'Step 4. Filter by HLA haplotype:'
        st.subheader(label_two)
        hla_haplotype_genes =   hla_query.split('~')
        form_two_list = {}
        haplotype_alleles   =   {}
        

        hla_gene_hap  = st.radio(
            'Choose one HLA gene to filter by its allele options ',
            hla_haplotype_genes,
            key='hla_hap_genes'
        )

        for index, hla_gene in enumerate(hla_haplotype_genes):
            form_two_list[hla_gene]  =   sorted( dataframe.iloc[:, index ].astype(str).unique() )

        if hla_gene_hap:
            alleles_chosen = st.multiselect('Choose the HLA-'+ hla_gene_hap +' allele',form_two_list[hla_gene_hap], key= hla_gene_hap)

    
    
    button_one  =   st.button('Submit')


col_one, col_two = st.columns(2)


if button_one:
    if choice_hap_or_al[answer_one]   ==  'allele':
        with col_one:
            st.header("Main Table")
            csv = convert_df(dataframe)

            st.download_button(
                label="Download this table data as CSV",
                data=csv,
                file_name='table.csv',
                mime='text/csv',
                key='main_dataframe'
            )
            st.dataframe(dataframe, 2000, 700)
        
        if alleles_chosen:
            with col_two:
                st.header("Filtered Table")
                subframe    =   table_filter(dataframe, alleles_chosen)
                csv = convert_df(subframe)

                st.download_button(
                    label="Download this table data as CSV",
                    data=csv,
                    file_name='table.csv',
                    mime='text/csv',
                    key='subframe'
                )

                st.dataframe(subframe, 2000, 700)
    else:
        with col_one:
            st.header("Main Table")
            csv = convert_df(dataframe)

            st.download_button(
                label="Download this table data as CSV",
                data=csv,
                file_name='table.csv',
                mime='text/csv',
                key='main_dataframe'
            )
            st.dataframe(dataframe, 2000, 700)
        
        if alleles_chosen:
            with col_two:
                st.header("Filtered Table")
                col_index = hla_haplotype_genes.index(hla_gene_hap)
                col =   dataframe.columns[col_index]
                subframe    =   dataframe[dataframe[col].isin(alleles_chosen)]
                csv = convert_df(subframe)

                st.download_button(
                    label="Download this table data as CSV",
                    data=csv,
                    file_name='table.csv',
                    mime='text/csv',
                    key='subframe'
                )

                st.dataframe(subframe, 2000, 700)

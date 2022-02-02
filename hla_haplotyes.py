import pandas as pd
import glob
import streamlit as st

choice_hap_or_al    =   {
    # 'Choose an option':'empty',
    'ALLELE frequency': 'allele',
    'HAPLOTYPE frequency': 'haplotype' 
    }

choice_database    =   {
    # 'Choose an option':'empty',
    'NMDP database': 'nmdp',
    '17th Workshop - families': 'family',
    '17th Workshop - unrelated': 'unrelated' 
    }

# Workshop data dictionaries
alleles_workshop =   {
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
    'A~C~B~DRB345~DRB1~DQA1~DQB1~DPA1~DPB1':  'Global_Full_Haplotype_Summary_2018-07-31.xlsx'
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


# NMDP data dictionaries
path_nmdp_data  =   './nmdp_database/'
nmdp_alleles    =   {
    'HLA-A':        'A.xls',
    'HLA-C':        'C.xls',
    'HLA-B':        'B.xls',
    'HLA-DRB1':     'DRB1.xls',
    'HLA-DQB1':     'DQB1.xls',
    'HLA-DRB3/4/5': 'DRB3-4-5.xls',
}

nmdp_haplotypes =   {
    'A~B':                          'A_B.xls',
    'C~B':                          'C_B.xls',
    'B~DRB1':                       'B_DRB1.xls',
    'A~C~B':                        'A_C_B.xls',
    'A~C~B~DRB1':                   'A_C_B_DRB1.xls',
    'A~B~DRB1':                     'A_B_DRB1.xls',
    'A~B~DRB1~DQB1':                'A_B_DRB1_DQB1.xls',
    'A~C~B~DRB1~DQB1':              'A_C_B_DRB1_DQB1.xls',
    'A~C~B~DRB345~DRB1~DQB1':       'A_C_B_DRB3-4-5_DRB1_DQB1.xls',
    'C~B~DRB1~DQB1':                'C_B_DRB1_DQB1.xls',
    'DRB1~DQB1':                    'DRB1_DQB1.xls',
    'DRB345~DQB1':                  'DRB3-4-5_DQB1.xls',
    'DRB345~DRB1':                  'DRB3-4-5_DRB1.xls',
    'DRB345~DRB1~DQB1':             'DRB3-4-5_DRB1_DQB1.xls',
}

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep=';').encode('utf-8')

## Functions to look for the apropriate table
# 17th workshop family data
def family_df(hap_or_allele, hla_query):
    if hap_or_allele == 'allele':
        table = alleles_workshop[hla_query] 
    else:
        table   =   family_haplotypes[hla_query]

    path_file   =   path_family_data + table
    df   =   pd.read_excel(path_file, header=[3,4,5])
    return df

# 17th workshop unrelated data
def unrelated_df(hap_or_allele, hla_query):
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

# NMDp data
def nmdp_df(hap_or_allele, hla_query):
    if hap_or_allele == 'allele':
        table = nmdp_alleles[hla_query] 
    else:
        table   =   nmdp_haplotypes[hla_query]

    path_file   =   path_nmdp_data + table
    df   =   pd.read_excel(path_file)
    return df

## Function to ask for the apropriate dataframe
def table_search(hap_or_allele, fam_or_unr, hla_query ):
    if fam_or_unr == 'family':
        df   =   family_df(hap_or_allele, hla_query)
    elif fam_or_unr == 'unrelated':
        df   =   unrelated_df(hap_or_allele, hla_query)

    else:
        df   =   nmdp_df(hap_or_allele, hla_query)
    return df

## Function to filter df lines according to HLA alleles informed by user
def table_filter(dataframe, args_list):
    col =   dataframe.columns[0]
    return dataframe.loc[dataframe[col].isin(args_list)]


#### Page starts here
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
def expander_nmdp():
    with st.expander("For detailed information regarding 17th Workshop data, please refers to:"):
        # st.image("./media/IHIWS_logo.png")
        st.write("""Title: High-resolution HLA allele and haplotype frequencies in several unrelated populations determined
        by next generation sequencing: 17th International HLA and Immunogenetics Workshop joint report""")
        st.write("Human Immunology, Volume 82, Issue 7, 2021, Pages 505-522")
        st.write("""Authors: Lisa E. Creary, Nicoletta Sacchi, Michela Mazzocco, Gerald P. Morris, Gonzalo Montero-Martin, Winnie Chong,
        Colin J. Brown, Amalia Dinou, Catherine Stavropoulos-Giokas, Clara Gorodezky, Saranya Narayan, Srinivasan Periathiruvadi,
        Rasmi Thomas, Dianne De Santis, Jennifer Pepperall, Gehad E. ElGhazali, Zain Al Yafei, Medhat Askar, Shweta Tyagi, Uma Kanga,
        Susana R. Marino, Dolores Planelles, Chia-Jung Chang, Marcelo A. Fernández-Viña""")
        st.write("""
        Abstract: The primary goal of the unrelated population HLA diversity (UPHD) component of the 17th International HLA and Immunogenetics Workshop was
        to characterize HLA alleles at maximum allelic-resolution in worldwide populations and re-evaluate patterns of HLA diversity across populations.
        The UPHD project included HLA genotype and sequence data, generated by various next-generation sequencing methods,
        from 4,240 individuals collated from 12 different countries.
        Population data included well-defined large datasets from the USA and smaller samples from Europe, Australia, and Western Asia. Allele and haplotype
        frequencies varied across populations from distant geographical regions. HLA genetic diversity estimated at 2- and 4-field allelic resolution revealed
        that diversity at the majority of loci, particularly for European-descent populations, was lower at the 2-field resolution. Several common alleles with identical
        protein sequences differing only by intronic substitutions were found in distinct haplotypes, revealing a more detailed characterization of linkage between variants
        within the HLA region. The examination of coding and non-coding nucleotide variation revealed many examples in which almost complete biunivocal relations between common
        alleles at different loci were observed resulting in higher linkage disequilibrium. Our reference data of HLA profiles characterized at maximum resolution from many populations
        is useful for anthropological studies, unrelated donor searches, transplantation, and disease association studies.
        """)
        with open('media/NMDP_Population.pdf', 'rb') as f:
           st.download_button('Check this pdf file for more information', f, file_name='NMDP_population_info.pdf')  # Defaults to 'application/octet-stream'

 

def expander_workshop(family_or_unrelated):
    with st.expander("For detailed information regarding NMDP data, please refers to:"):
        # st.image("./media/Be_The_Match.jpg")
        st.write("""Title: Six-locus high resolution HLA haplotype frequencies derived from mixed-resolution DNA typing for the entire US donor registry.""")
        st.write("Human Immunology, 74(10), 1313–1320.")
        st.write("""Authors: Gragert, L., Madbouly, A., Freeman, J., & Maiers, M.""")
        st.write("""Abstract: We have calculated six-locus high resolution HLA A∼C∼B∼DRB3/4/5∼DRB1∼DQB1 haplotype frequencies using all Be The Match® Registry
        volunteer donors typed by DNA methods at recruitment. Mixed resolution HLA typing data was inputted to a modified expectation–maximization (EM) algorithm
        in the form of genotype lists generated by interpretation of primary genomic typing data to the IMGT/HLA v3.4.0 allele list.
        The full cohort consists of 6.59 million subjects categorized at a broad race level. Overall 25.8% of the individuals were typed at the C locus,
        and 5.2% typed at the DQB1 locus, while all individuals were typed for A, B, DRB1. We also present a subset of 2.90 million subjects
        with detailed race/ethnic information mapped to 21 population subgroups, 64.1% of which have primary DNA typing data across at least A, B, and DRB1 loci.
        Sample sizes at the detailed race level range from 1,242,890 for European Caucasian to 1,376 Alaskan Native or Aleut. Genetic distance measurements
        show high levels of HLA genetic divergence among the 21 detailed race categories, especially among the eight Asian–American populations.
        These haplotype frequencies will be used to improve match predictions for donor selection algorithms for hematopoietic stem cell transplantation
        and improve the accuracy in modeling registry match rates.""")
        if family_or_unrelated == 'family':
            readme_file = 'media/Readme-Family-HLA-allele-and-haplotypes-FQ-tables.pdf'
            file_name   =  'Workshop_Family_Data_readme.pdf'
        else:
            readme_file = 'media/Readme-Unrelated-HLA-allele-and-haplotypes-FQ-tables_072318.pdf'
            file_name   =  'Workshop_Unrelated_Data_readme.pdf'
        with open(readme_file, 'rb') as f:
            st.download_button('Check this pdf file for more information', f, file_name = file_name)  # Defaults to 'application/octet-stream'



with st.sidebar:
    # with st.form('form_one'):
    st.title('HLA alleles/haplotypes frequency explorer')
    
    # Choose between haplotype or individual allele frequency
    st.subheader('Step 1. Choose among single HLA allele or haplotype frequency:')
    answer_hap_or_al  = st.radio(
        'single HLA allele or Haplotype frequency',
        choice_hap_or_al.keys(),
        key='hap_allele'
        )
    
    # Choose between nmdp, WORKSHOP-family or WORKSHOP-unrelated
    st.subheader('Step 2. Choose the database:')
    answer_database  = st.radio(
        'Data from the NMDP or the 17th HLA workshop',
        choice_database.keys(),
        key='database'
        )
    

    if choice_database[answer_database] == 'family':
        #Choice WORKSHOP - family
        if choice_hap_or_al[answer_hap_or_al] == 'allele':
            #Choice allele frequency
            st.subheader('Step 3. Choose the HLA gene:')
            hla_query  = st.selectbox(
                'Choose the HLA gene :',
                alleles_workshop.keys(),
                key='hla_allele',
                )
        else:
            # Choice haplotype
            st.subheader('Step 3. Choose the HLA Haplotype:')
            hla_query  = st.selectbox(
                'Choose the HLA haplotype :',
                family_haplotypes.keys(),
                key='hla_allele',
                )

    elif choice_database[answer_database] == 'unrelated':
        #Choice WORKSHOP - unrelated
        if choice_hap_or_al[answer_hap_or_al]   ==  'haplotype':
            #Choice haplotype frequency
            st.subheader('Step 3. Choose the HLA Haplotype:')
            hla_query  = st.selectbox(
                'Choose the HLA haplotype :',
                unrelated_haplotypes.keys(),
                key='hla_allele',
                )
        else:
            st.subheader('Step 3. Choose the HLA gene:')
            # Choose which HLA gene
            hla_query  = st.selectbox(
                'Choose the HLA gene :',
                alleles_workshop.keys(),
                key='hla_allele',
                )

    else:
        #Choice NMDP database
        if choice_hap_or_al[answer_hap_or_al]   ==  'allele':
            # Choose which HLA gene
            st.subheader('Step 3. Choose the HLA gene:')
            hla_query  = st.selectbox(
                'Choose the HLA gene :',
                nmdp_alleles.keys(),
                key='hla_allele',
                )
        else:
            st.subheader('Step 3. Choose the HLA Haplotype:')
            hla_query  = st.selectbox(
                'Choose the HLA haplotype :',
                nmdp_haplotypes.keys(),
                key='hla_allele',
                )

    dataframe   =   table_search(
        choice_hap_or_al[answer_hap_or_al],
        choice_database[answer_database],
        hla_query
        )


    if choice_hap_or_al[answer_hap_or_al]   ==  'allele':
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


col_one, col_two = st.columns([2,3])


if button_one:
    if choice_database[answer_database] == 'nmdp':
        expander_nmdp()
    else:
        expander_workshop(choice_database[answer_database])
    
    if choice_hap_or_al[answer_hap_or_al]   ==  'allele':
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
            st.dataframe(dataframe.sort_values(dataframe.columns[0]), 2000, 700)
        
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
                subframe    =   dataframe[dataframe[col].isin(alleles_chosen)].sort_values(col)
                csv = convert_df(subframe)

                st.download_button(
                    label="Download this table data as CSV",
                    data=csv,
                    file_name='table.csv',
                    mime='text/csv',
                    key='subframe'
                )

                st.dataframe(subframe, 2000, 700)


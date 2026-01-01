import streamlit as st
import pandas as pd
import time

def progress_bar():
    #Make a progress bar
    bar = st.progress(value=0)
    for i in range(100):
        time.sleep(0.05)
        bar.progress(i)
    bar.empty()

def column_remover(df, remove_columns):
    df = df.drop(columns = remove_columns)
    progress_bar()
    st.session_state['column_removed'] = df
    
def list_subtract(l1, l2):
    temp = []
    for i, j in zip(l1, l2):
        if i not in l2:
            temp.append(i)
    return temp

def view_data(file):
    extension = file.name.split('.')[1]

    if extension == "csv":
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.session_state['data'] = data

#Set the title
st.title("Data Cleaning")
st.markdown("---")

#file upload
st.markdown("""
<style>
    #file_uploader
    {
        font-size: 20px;
        color: #ffffff;        
    }
</style>
<p id='file_uploader'>Please upload your file</p>
""", unsafe_allow_html=True)
file = st.file_uploader("Please upload your file", key='file_uploader', 
                                 label_visibility="collapsed",
                                 type=('csv', 'xls', 'xlsx', 'xlsm', 'xlsb'))

c1, c2, c3 = st.columns([1, 0.3, 1])

if file is not None:
    with c1:
        view_data_button = st.button("view", key='view_data', on_click=view_data, args=(file,))
    if 'data' in st.session_state:
        st.dataframe(pd.DataFrame(st.session_state['data']))
        df = pd.DataFrame(st.session_state['data'])
        st.markdown("---")
        st.markdown("""
        <style>
            #show_column_headers
            {
                font-size: 35px;
                color: #76FF03;        
            }
        </style>
        <p id='show_column_headers'>Columns</p>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns([0.75, 1.25])
        with c1:     
            st.write(df.columns)
        with c2:
            all_columns = list(df.columns)
            selected_cols = st.multiselect("Select columns to keep:", all_columns)
            sub_c1, sub_c2 = st.columns([1, 1])
            with sub_c1:
                st.write("you selected: ", selected_cols)

        remove_columns = list_subtract(all_columns, selected_cols)
        with sub_c2:
            st.write("columns to be removed: ", remove_columns)
        column_remove_button = st.button("Remove Columns",
                                          key="column_remove_button",
                                          on_click=column_remover,
                                          args=(df, remove_columns,))
        st.dataframe(st.session_state['column_removed'])


        st.markdown("---")
        st.markdown("""
        <style>
            #show_column_headers
            {
                font-size: 35px;
                color: #76FF03;        
            }
        </style>
        <p id='show_column_headers'>Duplicates</p>
        """, unsafe_allow_html=True)
        
        
else:
    st.warning("please upload a file")








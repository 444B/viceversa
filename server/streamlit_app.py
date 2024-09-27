import streamlit as st
import sqlite3
import pandas as pd
import os

def load_data(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM data", conn)
    conn.close()
    return df

def main():
    st.title("Server Data Viewer")
    db_path = os.path.join(os.path.dirname(__file__), 'db/main_sql.db')
    df = load_data(db_path)
    st.dataframe(df)

if __name__ == '__main__':
    main()

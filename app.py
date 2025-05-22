import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="E-Shop Brasil - Big Data", layout="wide")

# Conexão com o MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["eshop"]
collection = db["clientes"]

st.title("📦 E-Shop Brasil - Gestão de Dados com MongoDB")

menu = st.sidebar.radio("Menu", ["Inserir", "Visualizar", "Editar", "Deletar"])

if menu == "Inserir":
    st.subheader("Adicionar novo cliente")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    cidade = st.text_input("Cidade")
    if st.button("Salvar"):
        collection.insert_one({"nome": nome, "email": email, "cidade": cidade})
        st.success("Cliente adicionado com sucesso!")

elif menu == "Visualizar":
    st.subheader("Visualizar todos os clientes")
    data = list(collection.find())
    df = pd.DataFrame(data)
    if not df.empty:
        df.drop(columns=["_id"], inplace=True)
        st.dataframe(df)
    else:
        st.warning("Nenhum dado encontrado.")

elif menu == "Editar":
    st.subheader("Editar cliente")
    email = st.text_input("Email do cliente a editar")
    novo_nome = st.text_input("Novo nome")
    if st.button("Atualizar"):
        result = collection.update_one({"email": email}, {"$set": {"nome": novo_nome}})
        if result.matched_count > 0:
            st.success("Cliente atualizado!")
        else:
            st.error("Cliente não encontrado.")

elif menu == "Deletar":
    st.subheader("Remover cliente")
    email = st.text_input("Email do cliente a deletar")
    if st.button("Deletar"):
        result = collection.delete_one({"email": email})
        if result.deleted_count > 0:
            st.success("Cliente removido com sucesso!")
        else:
            st.error("Cliente não encontrado.")
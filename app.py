import streamlit as st
from src.services.blob_service import upload_to_blob
from src.services.credit_card_service import analyze_credit_card



def configure_interface():
    st.title("Document Upload de Arquivo DIO Desafio Azure - Fake Docs")
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        fileName = uploaded_file.name
        # enviar para o Azure Blob Storage
        blob_url = upload_to_blob(uploaded_file, fileName)
        if blob_url is not None:
            st.success(f"Arquivo '{fileName}' enviado com sucesso!")
            st.write(f"URL do arquivo: {blob_url}")
            st.image(uploaded_file, caption='Imagem enviada', use_container_width=True)
            credit_card_number = analyze_credit_card(blob_url)  # Chamar a função que extrai o número do cartão
            show_image_validation = st.checkbox("Validar imagem", value=False)
            # Aqui você pode chamar a função de validação se o checkbox for marcado
            if show_image_validation:
                extract_credit_card_number(blob_url, credit_card_number)
        else:
            st.error("Erro ao enviar o arquivo.")

def extract_credit_card_number(blob_url, credit_card_number):
    # Função para extrair o número do cartão de crédito usando OCR
    st.image(blob_url, caption='Imagem enviada', use_column_width=True)
    st.write("Resultado da validação:")
    if credit_card_number and credit_card_number.get("card_number"):
        st.markdown(f"Número do cartão de crédito extraído: {credit_card_number['card_number']}")
        st.write(f"Nome do titular: {credit_card_number.get('card_holder_name', 'N/A')}")
        st.write(f"Data de validade: {credit_card_number.get('expiry_date', 'N/A')}")
        st.write(f"Bandeira: {credit_card_number.get('brand', 'N/A')}")
    else:
        st.error("Não foi possível extrair o número do cartão de crédito.")

if __name__ == "__main__":
    configure_interface()
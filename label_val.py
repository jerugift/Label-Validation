import re
import streamlit as st
import base64
from PIL import Image
import pytesseract
import pandas as pd


# install tesseract from here and add to path :  https://github.com/UB-Mannheim/tesseract/wiki


# Example rules stored in a dictionary
rules = {
    "Rule-1": "Drug Facts",
    "Rule-2": "Drug Facts (continued)",    
    "Rule-3": "Active ingredients",    
    "Rule-4": "Purposes",    
    "Rule-5": "Uses",   
    "Rule-6": "Warnings",
    "Rule-7": "Do not use",
    "Rule-8": "Ask a doctor or pharmacist before use",
    "Rule-9": "When using this product",
    "Rule-10": "Stop use and ask a doctor if",
    "Rule-11": "Directions",
    "Rule-12": "Other information",
    "Rule-13": "Inactive ingredients",
    "Rule-14": "Questions or comments?"

}

other_rules = {
    "Rule-2": " Drug Facts (continued)",    
    "Rule-3": "Active ingredient",
    "Rule-4": "Purpose",
    "Rule-5": "Use",
    "Rule-6": "Warning",
    "Rule-14": "Questions?"
}

#Validation
def validate_label(text, rules):
    report = {}
    for rule_name, rule_pattern in rules.items():
        if re.search(rule_pattern, text):
            report[rule_pattern] = "Yes"
        elif rule_name in other_rules.keys():
            if re.search(other_rules[rule_name], text):
                report[other_rules[rule_name]] = "Yes"
            else:
                report[rule_pattern] = "No"
        else:
            report[rule_pattern] = "No"
    return report

# Streamlit UI
def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

page_bg=f"""
   <style>   
    [data-testid="stAppViewContainer"] {{
    background: linear-gradient(180deg, #dbdeff, #dbdeff, #687eff);}}  

    </style>
   """

text_bg=f"""
   <style>   
    [data-testid="stHeading"] {{
    style="text-align:left";}}  

    </style>
   """

st.markdown(page_bg, unsafe_allow_html=True)
st.title(":blue[Label Validation System]")


# Input for drug name
details = st.text_input("Enter the name of your Drug:")

# File uploader for text files (single file)
uploaded_file = st.file_uploader("Please upload your label (text file)", type=['jpg', 'png', "jpeg", 'jfif'])

if uploaded_file is not None:
    # Read and display the uploaded file content
    img = Image.open(uploaded_file)

    # Display the image in the app
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Perform OCR using pytesseract
    extracted_text = pytesseract.image_to_string(img)

    # Display the extracted text
    st.subheader('Extracted Text')
    text=st.text_area("Label Content", extracted_text, height=300)

    #Validation button
    if st.button("Validate", type='primary', disabled=False, ):
     # Perform label validation
        validation_report = validate_label(text, rules)
        
    # Display the validation report
        st.header("Validation Report")
        v_report=pd.DataFrame.from_dict(validation_report, orient='index')
        table_bg=f"""
   <style>   
    [data-testid="stTableStyledTable"] {{
    background: linear-gradient(180deg, #dbdeff, #dbdeff, #687eff);}}  

    </style>
   """
        st.table(v_report)

else:
    st.write("Please upload an image to validate.")
    st.button("Validate", type='primary', disabled=True)
 
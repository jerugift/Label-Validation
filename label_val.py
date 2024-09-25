import re
import streamlit as st
import base64
from PIL import Image
import pytesseract
import pandas as pd
import zipfile
import os
import tempfile


rules = {
    "Rule-1": "Drug Facts",
    "Rule-2": r"Drug Facts\s*\(continued\)",    
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
            if rule_pattern==r"Drug Facts\s*\(continued\)":
                report["Drug Facts (continued)"] = "Yes"
            else:
                report[rule_pattern] = "Yes"
        elif rule_name in other_rules.keys():
            if re.search(other_rules[rule_name], text):
                if other_rules[rule_name]==r"Drug Facts\s*\(continued\)":
                    report["Drug Facts (continued)"] = "Yes"
                else:
                    report[other_rules[rule_name]] = "Yes"
            else:
                if rule_pattern==r"Drug Facts\s*\(continued\)":
                    report["Drug Facts (continued)"] = "No"
                else:
                    report[rule_pattern] = "No"
        else:
            if rule_pattern==r"Drug Facts\s*\(continued\)":
                report["Drug Facts (continued)"] = "No"
            else:
                report[rule_pattern] = "No"

    return report

def val_report(text_df):
    
    #Validation button
    if st.button("Validate", type='primary', disabled=False, ):
        st.header("Validation Report")
        # Perform label validation
        for content in range(len(text_df)):
            validation_report = validate_label(text_df['Extracted Content'][content], rules)
        
            # Display the validation report
            st.subheader(text_df['Image No.'][content])
            v_report=pd.DataFrame(list(validation_report.items()), columns=['Labels', 'Presence/Absence of Labels'])
            df=v_report.style.applymap('background-color: white')
            st.dataframe(v_report)


    return "Done"


def text_extraction(uploaded_file):

    labels_df=[]
    image_name='Image-0'
    final_labels_df=None

    if uploaded_file is not None:
        
        # Load the uploaded image
        for i in range(len(uploaded_file)):
            img = Image.open(uploaded_file[i])
            
            image_no=int(image_name[6:])+1
            image_name=f'Image-{image_no}'
            # Display the image in the app
            st.image(img, caption='Uploaded Image', use_column_width=True)

            # Perform OCR using pytesseract
            extracted_text = pytesseract.image_to_string(img)

            # Display the extracted text
            st.subheader(f'Extracted Text for {image_name}')
            text=st.text_area("Label Content", extracted_text, height=300)            
            label_text_df= pd.DataFrame({'Image No.': [image_name], 'Extracted Content': [text]})
            labels_df.append(label_text_df)
        
        if labels_df !=[]:
            print("LABEL")
            final_labels_df=pd.concat(labels_df, ignore_index=True)
            val_report(final_labels_df)

    else:
        st.write("Please upload an image to validate.")
        st.button("Validate", type='primary', disabled=True)

    return final_labels_df


def process_images(image_files):

    labels_df=[]
    final_labels_df=None

    if image_files is not None:
        for image_file in image_files:
            img = Image.open(image_file)
        
            # Display the image
            st.image(img, caption=f'Uploaded Image: {os.path.basename(image_file)}', use_column_width=True)
        
            # Perform OCR using pytesseract
            extracted_text = pytesseract.image_to_string(img)
        
            # Display the extracted text
            st.subheader(f'Extracted Text from {os.path.basename(image_file)}')        
            text=st.text_area("Label Content", extracted_text, height=300)            
            
            label_text_df= pd.DataFrame({'Image No.': [os.path.basename(image_file)], 'Extracted Content': [text]})
            labels_df.append(label_text_df)

        if labels_df !=[]:
            print("LABEL")
            final_labels_df=pd.concat(labels_df, ignore_index=True)
            val_report(final_labels_df)
    else:
        st.write("Please upload an image to validate.")
        st.button("Validate", type='primary', disabled=True)

    return final_labels_df


def main():

    page_bg=f"""
   <style>   
    [data-testid="stAppViewContainer"] {{
    background: linear-gradient(180deg, #dbdeff, #dbdeff, #687eff);}}  

    </style>
   """

    text_bg=f"""
    <style>   
        [data-testid="stHeading"] {{
        text-align: center;
        color: white;
        }}  

        </style>
    """

    st.markdown(page_bg, unsafe_allow_html=True)
    st.markdown(text_bg, unsafe_allow_html=True)
    
    st.title("Label Validation System")
    st.header("(OTC Drugs)")

    
    option = st.radio(
        "Choose the file type for uploading:",
        ('Single/Multiple Image(s)', 'Folder (Upload as zip)'))

    
    if option=='Single/Multiple Image(s)':
        uploaded_file = st.file_uploader("Please upload your labels", type=['jpg', 'png', "jpeg", 'jfif','webp'], accept_multiple_files=True )
        text_extraction(uploaded_file)
    

    elif option == 'Folder (Upload as zip)':
        uploaded_zip = st.file_uploader("Choose a zip file representing a folder", type="zip")

        if uploaded_zip is not None:
        # Extract the zip file
            with zipfile.ZipFile(uploaded_zip, 'r') as z:
                # Create a temporary directory to extract the files
                with tempfile.TemporaryDirectory() as temp_dir:
                    z.extractall(temp_dir)
    
                    # Recursively get a list of all image files in the extracted folder
                    image_files = []
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if file.endswith((".png", ".jpg", ".jpeg", ".jfif")):
                                image_files.append(os.path.join(root, file))
    
                    # Check if exactly 10 images are present
                    if len(image_files) <= 5:
                        process_images(image_files)
                    else:
                        st.error("The zip file must contain maximum 50 images. Please upload a zip file within 50 images.")

main()

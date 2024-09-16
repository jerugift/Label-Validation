# Label-Validation

### Label Validation System - README

#### Introduction
The **Label Validation System** is a Python-based application built using **Streamlit** for validating drug labels by extracting text from images and checking for the presence of specific regulatory content. It uses **pytesseract** to extract text from images and compares the extracted text against predefined rules to ensure regulatory compliance.

#### Features
1. **Image Upload:** Accepts images of drug labels in various formats (JPEG, PNG, JPG, JFIF).
2. **Text Extraction:** Uses **pytesseract** (OCR) to extract text from the uploaded image.
3. **Validation:** Validates the extracted text against predefined rules for regulatory content.
4. **User Interface:** Displays the image, extracted text, and validation results in a clean and intuitive interface using **Streamlit**.
5. **Background Customization:** Provides custom backgrounds for the app's appearance using CSS styles.
6. **Result Table:** Shows the validation report in a tabular format.

---

### Requirements

#### Libraries
Make sure the following Python libraries are installed:
- **Streamlit:** For building the web app UI
- **Pytesseract:** For performing Optical Character Recognition (OCR) on images
- **Pillow:** For image processing
- **pandas:** For handling and displaying data in tabular form
- **re:** Python's regular expression library

To install the required libraries, run:
```bash
pip install streamlit pytesseract pillow pandas
```

#### Tesseract Installation
For text extraction, **Tesseract** must be installed separately on your system. You can download and install it from [Tesseract GitHub page](https://github.com/UB-Mannheim/tesseract/wiki). After installation, make sure to add Tesseract to your system's PATH.

---

### Folder Structure

```
|-- app.py                  # Main Python file containing the Streamlit application
|-- README.md               # Documentation file
|-- requirements.txt        # List of Python dependencies
|-- assets/                 # Folder for storing background images
     |-- background.png     # Example background image used in the sidebar
```

---

### How to Run the App

1. **Install Tesseract**:
   Make sure Tesseract is installed and added to your system PATH.

2. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/label-validation-system.git
   cd label-validation-system
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   To start the app, run the following command in the terminal:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**:
   After running the command, open your browser and navigate to `http://localhost:8501`.

---

### Application Workflow

1. **Upload Image**:
   - The app allows you to upload a drug label image (JPG, PNG, JPEG, JFIF).
   
2. **Text Extraction**:
   - Once the image is uploaded, the app extracts text using **pytesseract** and displays it in a text area.

3. **Label Validation**:
   - On clicking the "Validate" button, the extracted text is checked against predefined rules to ensure mandatory sections (like 'Drug Facts', 'Warnings', 'Directions', etc.) are present.
   - The validation results are displayed in a table format, with each rule showing a "Yes" or "No" status.

---

### Rules for Validation

The rules are stored in a dictionary for easy modification. The primary rules (`rules`) and alternative forms of the rules (`other_rules`) are checked in sequence. If any rule from `other_rules` is found, it will be accepted as valid.

#### Predefined Rules:
```python
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
```

Alternative rule names (e.g., "Warning" instead of "Warnings") are handled in the `other_rules` dictionary.

---

### Customization

#### Background Image
To customize the background, you can update the `page_bg` variable with your desired colors or background image by modifying the CSS code in the script:
```python
page_bg=f"""
<style>   
[data-testid="stAppViewContainer"] {{
background: linear-gradient(180deg, #dbdeff, #dbdeff, #687eff);}}  
</style>
"""
```

You can also update the sidebar background by modifying the `sidebar_bg` function and passing the new image file.

---

### Known Limitations
1. **Image Quality**: The accuracy of text extraction depends on the quality of the uploaded image.
2. **Predefined Rules**: Validation is strictly based on predefined rules. It does not support user-defined rules as of now.
3. **Multiple File Uploads**: The current implementation only supports single file uploads for validation.

---

### Future Enhancements
1. **Multi-File Support**: Add the ability to validate multiple images at once.
2. **Dynamic Rules**: Allow users to define and modify validation rules through the UI.
3. **Better OCR Handling**: Improve the OCR functionality by adding options to preprocess the images (e.g., resizing, denoising) before extraction.

---

### License
This project is open-source and licensed under the MIT License.

---

Enjoy validating your drug labels!

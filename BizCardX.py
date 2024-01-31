import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import mysql.connector
from sqlalchemy import create_engine
import io

# Connect to MySQL server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Fluffy@53"
)
step = mydb.cursor()
step.execute('CREATE DATABASE if not exists bizcard')
step.execute('Use bizcard')

#Create a Table
step.execute("""
    CREATE TABLE IF NOT EXISTS business_card (
        NAME VARCHAR(50),
        DESIGNATION VARCHAR(100),
        COMPANY_NAME VARCHAR(100),
        CONTACT VARCHAR(100),
        EMAIL VARCHAR(100),
        WEBSITE VARCHAR(100),
        ADDRESS TEXT,
        PINCODE VARCHAR(100)
    )
""")
mydb.commit()

#Streamlit
st.set_page_config(layout="wide")
st.markdown("""
    <style>
            
        .dark-purple-title {
            background-color: rgba(255, 182, 193, 0.8); /* Transparent Light Pink */
            color: #8B0000; /* Dark Bluish Text Color */
            text-align: center; /* Center-align the text */
            font-size: 48px !important;
            font-weight: bold;
            padding: 15px;
            border-radius: 20px;

    </style>
    """, unsafe_allow_html=True)

st.markdown("<p class='dark-purple-title'<h1>BizCardX: Extracting Business Card Data with OCR</h1></div>", unsafe_allow_html=True)

#Background image
def background():
    st.markdown(f""" <style>.stApp {{
                        background: url("https://wallpaperaccess.com/full/1913844.jpg");
                        background-size: cover;
                    }}
                 </style>""", unsafe_allow_html=True)

background()

#Option Menu
selected = option_menu(None, ["Home", "Upload & Modify", "Delete"],
                       icons=["house", "upload", "trash"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "28px", "text-align": "center", "margin": "5px",
                                            "color": "#000", "border-radius": "15px", "padding": "10px", 
                                            "background-color": "#FFFAFA", "transition": "background-color 0.3s",
                                            "--hover-color": "#FA8072"},
                               "icon": {"font-size": "28px", "margin-right": "5px"},
                               "container": {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#CC0000"}})

# Home Menu
if selected == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="text-align: left;">
            <h2 style="color: red; text-decoration: underline;text-decoration-color: white; font-size: 40px;">About:</h2>
            <p style="font-size: 36px;">Bizcard is a Python application created with the primary purpose of extracting information from business cards.</p>
            <p style="font-size: 36px;">The main purpose of Bizcard is to automate the process of extracting key details from business card images:</p>
            <ul>
                <li style="font-size: 36px;">Name</li>
                <li style="font-size: 36px;">Designation</li>
                <li style="font-size: 36px;">Company</li>
                <li style="font-size: 36px;">Contact Information</li>
                <li style="font-size: 36px;">Other relevant data</li>
            </ul>
            <p style="font-size: 36px;">By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.image(Image.open("C:\\Users\\Sujay\\New folder\\bizcard.jpg"), width=750)
        st.markdown("""
        <div style="text-align: right;">
            <h1 style="color: red; text-decoration: underline;text-decoration-color: white;">Technologies Used:</h1>
            <p style="font-size: 36px;"> Python</p>
            <p style="font-size: 36px;"> Easy OCR</p>
            <p style="font-size: 36px;"> Streamlit</p>
            <p style="font-size: 36px;"> SQL</p>
            <p style="font-size: 36px;"> Pandas</p>
        </div>
        """, unsafe_allow_html=True)
                          
#Data Extraction
def extracted_text(picture):
    extracted_dict = {'Name': [], 'Designation': [], 'Company name': [], 'Contact': [], 'Email': [], 'Website': [],
               'Address': [], 'Pincode': []}

    extracted_dict['Name'].append(result[0])
    extracted_dict['Designation'].append(result[1])

    for i in range(2, len(result)):
        if result[i].startswith('+') or (result[i].replace('-', '').isdigit() and '-' in result[i]):
            extracted_dict['Contact'].append(result[i])

        elif '@' in result[i] and '.com' in result[i]:
            small = result[i].lower()
            extracted_dict['Email'].append(small)

        elif 'www' in result[i] or 'WWW' in result[i] or 'wwW' in result[i]:
            small = result[i].lower()
            extracted_dict['Website'].append(small)

        elif 'Karnataka' in result[i] or 'Karnataka' in result[i] or result[i].isdigit():
            extracted_dict['Pincode'].append(result[i])

        elif re.match(r'^[A-Za-z\s&]+$', result[i]):
            extracted_dict['Company name'].append(result[i])

        else:
            removed_colon = re.sub(r'[.,;]', '', result[i])
            extracted_dict['Address'].append(removed_colon)

    for key, value in extracted_dict.items():
        if len(value) > 0:
            concatenated_string = ' '.join(value)
            extracted_dict[key] = [concatenated_string]
        else:
            value = 'NA'
            extracted_dict[key] = [value]

    return extracted_dict

#Upload and Modify option
if selected == "Upload & Modify":
    image = st.file_uploader(label="Upload your image", type=['png', 'jpg', 'jpeg'], label_visibility="hidden")

    @st.cache_data
    def load_image():
        reader = easyocr.Reader(['en'], model_storage_directory=".")
        return reader

    picture = load_image()
    if image is not None:
        input_image = Image.open(image)
       
        st.image(input_image, width=750)
        st.markdown(
            f'<style>.css-1aumxhk img {{ max-width: 300px; }}</style>',
            unsafe_allow_html=True
        )
        result = picture.readtext(np.array(input_image), detail=0)
        #coverting to pandas DataFrame
        ext_text = extracted_text(result)
        df = pd.DataFrame(ext_text)
        st.dataframe(df)
        # Converting image into bytes
        image_bytes = io.BytesIO()
        input_image.save(image_bytes, format='PNG')
        image_data = image_bytes.getvalue()
        # Creating dictionary
        data = {"Image": [image_data]}
        df_1 = pd.DataFrame(data)
        concat_df = pd.concat([df, df_1], axis=1)

        # Database
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            selected = option_menu(
                menu_title=None,
                options=["Preview"],
                icons=['file-earmark'],
                default_index=0,
                orientation="horizontal"
            )

            ext_text = extracted_text(result)
            df = pd.DataFrame(ext_text)

        if selected == "Preview":
            col_1, col_2 = st.columns([4, 4])
            with col_1:
                modified_name = st.text_input('Name', ext_text["Name"][0])
                modified_designation = st.text_input('Designation', ext_text["Designation"][0])
                modified_company = st.text_input('Company name', ext_text["Company name"][0])
                modified_contact = st.text_input('Mobile', ext_text["Contact"][0])
                concat_df["Name"], concat_df["Designation"], concat_df["Company name"], concat_df[
                    "Contact"] = modified_name, modified_designation, modified_company, modified_contact
            with col_2:
                modified_mail = st.text_input('Email', ext_text["Email"][0])
                modified_website = st.text_input('Website', ext_text["Website"][0])
                modified_address = st.text_input('Address', ext_text["Address"][0][1])
                modified_pincode = st.text_input('Pincode', ext_text["Pincode"][0])
                concat_df["Email"], concat_df["Website"], concat_df["Address"], concat_df[
                    "Pincode"] = modified_mail, modified_website, modified_address, modified_pincode

            col3, col4 = st.columns([4, 4])
            with col3:
                Preview = st.button("Preview modified text")
            with col4:
                Upload = st.button("Upload")
            if Preview:
                filtered_df = concat_df[
                    ['Name', 'Designation', 'Company name', 'Contact', 'Email', 'Website', 'Address', 'Pincode']]
                st.dataframe(filtered_df)
            else:
                pass

            if Upload:
                with st.spinner("In progress"):
                    step.execute(
                        "CREATE TABLE IF NOT EXISTS BUSINESS_CARD(NAME VARCHAR(50), DESIGNATION VARCHAR(100), "
                        "COMPANY_NAME VARCHAR(100), CONTACT VARCHAR(100), EMAIL VARCHAR(100), WEBSITE VARCHAR("
                        "100), ADDRESS TEXT, PINCODE VARCHAR(100))")
                    mydb.commit()
                    A = "INSERT INTO BUSINESS_CARD(NAME, DESIGNATION, COMPANY_NAME, CONTACT, EMAIL, WEBSITE, ADDRESS, " \
                        "PINCODE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    for index, i in concat_df.iterrows():
                        result_table = (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
                        step.execute(A, result_table)
                        mydb.commit()
                        st.success('SUCCESSFULLY UPLOADED', icon="✅")
    else:
        st.write("Upload an image")

# Delete option
if selected == "Delete":
    col1, col2 = st.columns([4, 4])
    with col1:
        step.execute("SELECT NAME FROM BUSINESS_CARD")
        Y = step.fetchall()
        names = ["Select"]
        for i in Y:
            names.append(i[0])
        name_selected = st.selectbox("Select the name to delete", options=names)
        # st.write(name_selected)
    with col2:
        step.execute(f"SELECT DESIGNATION FROM BUSINESS_CARD WHERE NAME = '{name_selected}'")
        Z = step.fetchall()
        designation = ["Select"]
        for j in Z:
            designation.append(j[0])
        designation_selected = st.selectbox("Select the designation of the chosen name", options=designation)
    st.markdown(" ")
   
    col_a, col_b, col_c = st.columns([5, 3, 3])
    with col_b:
        remove = st.button("Clik here to delete")
    if name_selected and designation_selected and remove:
        step.execute(
            f"DELETE FROM BUSINESS_CARD WHERE NAME = '{name_selected}' AND DESIGNATION = '{designation_selected}'")
        mydb.commit()
        if remove:
            st.warning("RECORD DELETED", icon="🚨")
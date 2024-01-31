# BizCardX - Extracting Business Card Data with OCR

BizCardX is a user-friendly tool for extracting information from business cards using Optical Character Recognition (OCR) technology. This project leverages the EasyOCR library to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. The extracted information is then accessible through a GUI built using Streamlit. The BizCardX application provides an intuitive interface for users to upload business card images, extract information, and manage the data within a database.

## Project Overview

BizCardX aims to simplify the process of extracting and managing information from business cards. The tool offers the following features:

- Extraction of key information from business cards: company name, cardholder name, designation, contact details, etc.
- Storage of extracted data in a MySQL database for easy access and retrieval.
- GUI built with Streamlit for a user-friendly interface.
- User options to upload, extract, and modify business card data.

## Libraries/Modules Used

- `pandas`: Used to create DataFrames for data manipulation and storage.
- `mysql.connector`: Used to store and retrieve data from a MySQL database.
- `streamlit`: Used to create a graphical user interface for users.
- `easyocr`: Used for text extraction from business card images.


## Approach:
1. Install the required packages: You will need to install Python, Streamlit,
easyOCR, and MySQL.
2. Design the user interface: Create a simple and intuitive user interface using
Streamlit that guides users through the process of uploading the business
card image and extracting its information. You can use widgets like file
uploader, buttons, and text boxes to make the interface more interactive.
3. Implement the image processing and OCR: Use easyOCR to extract the
relevant information from the uploaded business card image. You can use
image processing techniques like resizing, cropping, and thresholding to
enhance the image quality before passing it to the OCR engine.
4. Display the extracted information: Once the information has been extracted,
display it in a clean and organized manner in the Streamlit GUI. You can use
widgets like tables, text boxes, and labels to present the information.
5. Implement database integration: Use a database management system like
SQLite or MySQL to store the extracted information along with the uploaded
business card image. You can use SQL queries to create tables, insert data,
and retrieve data from the database, Update the data and Allow the user to
delete the data through the streamlit UI
6. Test the application: Test the application thoroughly to ensure that it works as
expected. You can run the application on your local machine by running the
command streamlit run BizCardX.py in the terminal, where BizCardX.py is the name of
your Streamlit application file.

## Conclusion:

BizCardX provides an effective solution for business card data extraction and management. Its integration of EasyOCR, MySQL, and Streamlit offers a user-friendly experience, making it adaptable for various use cases. Follow the steps outlined in this README to get started and enhance your business card information organization in the digital era.

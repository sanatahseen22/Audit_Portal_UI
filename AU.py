
import io
import streamlit as st
import pandas as pd
from googletrans import Translator
import streamlit.components.v1 as components

# Set the page configuration
st.set_page_config(page_title='Audit Portal', layout='wide')

# Step 1: Add CSS for dark blue theme
dark_blue_theme = """
<style>
/* Set the overall background color */
body {
    background-color: #04385f; /* Dark blue color */
    color: black; /* Text color */
}

/* Streamlit components background */
.stApp {
    background-color: #04385f; /* Match the app background */
}

/* Sidebar customization */
.sidebar .sidebar-content {
    background-color: #a9639b; /* Darker shade of blue for sidebar */
    color: white;
}

/* Customize headings */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF; /* White text for headings */
}

/* Buttons */
button {
    background-color: #1C3A74; /* Slightly lighter blue for buttons */
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}

/* Inputs and text areas */
input, textarea, select {
    background-color: #1C3A74; /* Dark blue input fields */
    color: white;
    border: 1px solid white;
    border-radius: 5px;
}

/* Carousel and other custom areas */
.carousel {
    background-color: #1C3A74;
}

/* Adjust scrollbars */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-thumb {
    background: #1C3A74; /* Blue scrollbar thumb */
    border-radius: 6px;
}

::-webkit-scrollbar-track {
    background: #0A1A4A; /* Blue scrollbar track */
}
</style>
"""

# Step 2: Apply CSS
st.markdown(dark_blue_theme, unsafe_allow_html=True)

# Initialize the Google Translator
translator = Translator()


# Define the task status options
task_status_options = ['Fixed', 'Not Fixed', 'Correct']
# Define the comments options for 'Fixed', Correct and 'Not Fixed' task status
fixed_comments = ['Image', 'Item_name', 'Bullets', 'Product_Description', 'Technical Details', 'QnA', 'Competitor Website', 'Brand Website', 'Hierarchy']
not_fixed_comments = ['Values Unavailable', 'Invalid ASIN', 'Misclassified - Different Product', 'Misclassified - Accessory', 'Inconsistent', 'Partial values', 'Not Applicable', 'Clarity Needed']
correct_comments = ['Values Already Backfilled']


# File uploader to allow users to select their input file
uploaded_file = st.file_uploader("Upload your input Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the input data from the uploaded file
    input_data = pd.read_excel(uploaded_file)
    
    
    # Initialize the Google Translator
    translator = Translator()
    
    # Define the columns and their accepted values
    column_details = {
        'PASIN_size_attribute': input_data['PASIN_size_attribute'].tolist(),
        'product_type': input_data['product_type'].tolist(),
        'attribute': input_data['attribute'].tolist(),
        'Country': input_data['Country'].tolist(),
        'Keywords': input_data['Keywords'].tolist(),
        'Accepted_Values': input_data['Accepted_Values'].tolist(),
        'Attribute_Datatype': input_data['Attribute_Datatype'].tolist(),
        'Image_link': input_data['Image_link'].tolist(),
        'Item_name': input_data['Item_name'].tolist(),
        'Bullet_Point': input_data['Bullet_Point'].tolist(),
        'Product_Description': input_data['Product_Description'].tolist(),
        'brand_name': input_data['brand_name'].tolist()
    }
    

    
    def render_image_carousel(image_links):
        # Filter out empty or non-functioning links
        valid_links = [img.strip() for img in image_links if img.strip()]
        
        # If there are valid image links, render the carousel
        if valid_links:
            carousel_html = f"""
            <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css"/>
            <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick-theme.css"/>
            <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.min.js"></script>
            <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.min.js"></script>
            
            <style>
                /* Main carousel styling */
                .carousel {{
                    background-color: #f9f9f9;
                    padding: 10px;
                    margin-bottom: 20px;
                }}
                .carousel img {{
                    max-width: 80%;
                    height: auto;
                    display: block;
                    margin: auto;
                }}
    
                /* Thumbnail styling */
                .thumbnail-carousel {{
                    margin-top: 10px;
                }}
                .thumbnail-carousel img {{
                    width: 60px;
                    height: 60px;
                    object-fit: cover;
                    border: 2px solid transparent;
                    cursor: pointer;
                }}
                .thumbnail-carousel .slick-current img {{
                    border-color: #000; /* Highlight active thumbnail */
                }}
            </style>
            
            <div class="carousel">
                {''.join([f'<div><img src="{img}" style="width:400px;height:auto;"/></div>' for img in valid_links])}
            </div>
            
            <div class="thumbnail-carousel">
                {''.join([f'<div><img src="{img}"/></div>' for img in valid_links])}
            </div>
            
            <script type="text/javascript">
                $(document).ready(function() {{
                    // Initialize the main carousel
                    $('.carousel').slick({{
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        arrows: true,
                        autoplay: false,
                       
                        asNavFor: '.thumbnail-carousel' // Link to thumbnails
                    }});
    
                    // Initialize the thumbnail carousel
                    $('.thumbnail-carousel').slick({{
                        slidesToShow: {min(len(valid_links), 8)}, // Show up to 8 thumbnails
                        slidesToScroll: 1,
                        asNavFor: '.carousel', // Link to the main carousel
                        focusOnSelect: true,
                        arrows: true,
                    }});
                }});
            </script>
            """
            components.html(carousel_html, height=500)  # Adjust height for carousel and thumbnails
    
        # If no valid image links, display a placeholder
        else:
            st.markdown("""
                <div style="width:300px;height:200px;display:flex;align-items:center;justify-content:center;border:1px solid #ccc;">
                    <p>No images available</p>
                </div>
            """, unsafe_allow_html=True)


    
# Function to initialize session state values for each row, using unique keys for each index
    def initialize_session_state(index):
        # Check and initialize each session state variable for the row if not already set
        if f'task_status_{index}' not in st.session_state:
            st.session_state[f'task_status_{index}'] = 'Not Fixed'
        if f'attribute_value_{index}' not in st.session_state:
            st.session_state[f'attribute_value_{index}'] = ''
        if f'D_{index}' not in st.session_state:
            st.session_state[f'D_{index}'] = ''
        if f'W_{index}' not in st.session_state:
            st.session_state[f'W_{index}'] = ''
        if f'H_{index}' not in st.session_state:
            st.session_state[f'H_{index}'] = ''
        if f'T_{index}' not in st.session_state:
            st.session_state[f'T_{index}'] = ''
        if f'attribute_unit_{index}' not in st.session_state:
            st.session_state[f'attribute_unit_{index}'] = ''
        if f'comments_{index}' not in st.session_state:
            st.session_state[f'comments_{index}'] = 'Values Unavailable'
        if f'third_party_link_{index}' not in st.session_state:
            st.session_state[f'third_party_link_{index}'] = ''
    
    # Load the input file into session state if not already loaded
    if 'input_data' not in st.session_state and uploaded_file is not None:
        st.session_state.input_data = pd.read_excel(uploaded_file)
    
    # Function to save data from session state back to the input data DataFrame
    def save_row(index):
        input_data = st.session_state.input_data
    
        # Add necessary columns if they don't exist in input_data
        columns_to_add = ['Task_Status', 'Task_Comments', 'Values_L', 'D', 'W', 'H', 'Thickness', 'Units', 'Comments', '3P_Website_Link']
        for col in columns_to_add:
            if col not in input_data.columns:
                input_data[col] = ''
    
        # Update input_data with the session state values for the current row
        input_data.at[index, 'Task_Status'] = st.session_state[f'task_status_{index}']
        input_data.at[index, 'Task_Comments'] = st.session_state[f'comments_{index}']
        input_data.at[index, 'Values_L'] = st.session_state[f'attribute_value_{index}']
        input_data.at[index, 'D'] = st.session_state[f'D_{index}']
        input_data.at[index, 'W'] = st.session_state[f'W_{index}']
        input_data.at[index, 'H'] = st.session_state[f'H_{index}']
        input_data.at[index, 'Thickness'] = st.session_state[f'T_{index}']
        input_data.at[index, 'Units'] = st.session_state[f'attribute_unit_{index}']
        input_data.at[index, 'Comments'] = st.session_state[f'task_comment_{index}']
        input_data.at[index, '3P_Website_Link'] = st.session_state[f'third_party_link_{index}']
    
        # Save back to session state and notify the user
        st.session_state.input_data = input_data
        st.success(f"Row {index+1}: Data saved successfully!")
         
            
            # Function to generate a single downloadable file after all rows are processed
    def download_updated_file():
            # Create an in-memory buffer to save the updated DataFrame from session state
            buffer = io.BytesIO()
            st.session_state.input_data.to_excel(buffer, index=False, engine='xlsxwriter')
            buffer.seek(0)
        
            # Provide a single download link for the complete updated file
            st.download_button(
                label="Download Final Output File",
                data=buffer,
                file_name="final_updated_input_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    # Function to render a single row with input fields and validation logic
    def render_row(index):
        initialize_session_state(index)  # Ensure session state variables are initialized
    
        # Display item name
        st.subheader('Item Name')
        st.markdown(f"<div style='font-size: 14px; font-weight: bold;'>{translate_text(st.session_state.input_data['Item_name'][index])}</div>", unsafe_allow_html=True)
    
        # Extract image links for carousel display
        image_links_raw = st.session_state.input_data['Image_link'][index]
        
        # Ensure image_links_raw is a string before attempting to split
        if isinstance(image_links_raw, str) and image_links_raw.strip():
            image_links = image_links_raw.split(',')
        else:
            image_links = []  # Set to an empty list if no valid image links are found
        
        # Layout for the image carousel and ASIN info
        col_image, col_info = st.columns([1, 1])
        with col_image:
            render_image_carousel(image_links)
    
        with col_info:
            asin_hyperlink = create_hyperlink(column_details['PASIN_size_attribute'][index], column_details['Country'][index])
            st.markdown(f"""
               <div style='border: 3px solid #ccc; padding: 20px;'>
                   <strong>ASIN:</strong> {asin_hyperlink} <br>
                   <strong>Product Type:</strong> {column_details['product_type'][index]}<br>
                   <strong>Marketplace:</strong> {column_details['Country'][index]}<br>
                   <strong>Attribute:</strong> {column_details['attribute'][index]}<br>
                   <strong>Brand Name:</strong> {column_details['brand_name'][index]}<br>   
                   <strong>Keywords:</strong> {column_details['Keywords'][index]}<br>
                   <strong>Attribute Datatype:</strong> {input_data['Attribute_Datatype'][index]}<br>
                   <strong>Accepted Values:</strong> {column_details['Accepted_Values'][index]}
               </div>
            """, unsafe_allow_html=True)
            
        # Layout for Product Description
        st.subheader('Bullet Point')
        st.markdown(f'''
        <p style="font-size: 14px;">
            {translate_text(input_data["Bullet_Point"][index])}
        </p>
    ''', unsafe_allow_html=True)
    
        # Layout for Bullet Points
        st.subheader('Product Description')
        st.markdown(f'''
        <p style="font-size: 14px;">
            {translate_text(input_data["Product_Description"][index])}
        </p>
    ''', unsafe_allow_html=True)           
    
        # Bottom Section 
        col_value, col_d, col_w, col_h, col_t = st.columns([2, 1, 1, 1, 1])
        with col_value:
            st.text_input('Values_L:', key=f'attribute_value_{index}')
        with col_d:
            st.text_input('D:', key=f'D_{index}')
        with col_w:
            st.text_input('W:', key=f'W_{index}')
        with col_h:
            st.text_input('H:', key=f'H_{index}')
        with col_t:
            st.text_input('Thickness:', key=f'T_{index}')
        
        # 3rd Row for Unit and Comments fields
        col_unit, col_task_comments = st.columns([2, 6])
        with col_unit:
            st.text_input('Units:', key=f'attribute_unit_{index}')
        
        with col_task_comments:
            st.text_input('Comments:', key=f'task_comment_{index}')
    
        # Task Status, Comments, and 3P Website Link (in the next row)
        col_status, col_comments, col_website = st.columns([2, 4, 6])
    
        with col_status:
            st.selectbox('Task Status', task_status_options, key=f'task_status_{index}')
            
        with col_comments:
            if st.session_state[f'task_status_{index}'] == 'Fixed':
                st.selectbox('Task Comments', fixed_comments, key=f'comments_{index}')
            elif st.session_state[f'task_status_{index}'] == 'Not Fixed':
                st.selectbox('Task Comments', not_fixed_comments, key=f'comments_{index}')
            elif st.session_state[f'task_status_{index}'] == 'Correct':
                st.selectbox('Task Comments', correct_comments, key=f'comments_{index}')
        
        with col_website:
            st.text_input('3P Website Link', key=f'third_party_link_{index}')
    
        # Submit button with validation logic
        if st.button(f'Submit Row {index+1}'):
            validate_and_save_row(index)
    if 'saved_rows' not in st.session_state:
        st.session_state.saved_rows = set()            
        
    # Function to handle validation and saving of the row
    def validate_and_save_row(index):
        # Retrieve necessary details from session state
        attribute_type = st.session_state.input_data['Attribute_Datatype'][index]
        accepted_units = column_details['Accepted_Values'][index].split(',')
    
        # Check for conditional validation based on task status and attribute type
        if st.session_state[f'task_status_{index}'] in ['Fixed', 'Correct']:
            if attribute_type == 'Value+Unit':
                # Check that at least one of Value, D, W, H, or T fields is filled
                if not st.session_state[f'attribute_value_{index}'].strip() and not st.session_state[f'D_{index}'].strip() and not st.session_state[f'W_{index}'].strip() and not st.session_state[f'H_{index}'].strip() and not st.session_state[f'T_{index}'].strip():
                    st.error(f"Row {index+1}: One of Value, D, W, H, or T must be filled!")
                # Check if the unit is valid based on accepted values
                elif st.session_state[f'attribute_unit_{index}'] not in accepted_units:
                    st.error(f"Row {index+1}: Unit must be one of the accepted values: {', '.join(accepted_units)}")
                else:
                    save_row(index) # Save if all checks pass
                    st.session_state.saved_rows.add(index) 
    
            elif attribute_type in ['String', 'Values Only']:
                # Ensure Value is not empty
                if not st.session_state[f'attribute_value_{index}'].strip():
                    st.error("Value cannot be empty!")
                # Ensure Unit field is empty for String or Values Only types
                elif st.session_state[f'attribute_unit_{index}'].strip():
                    st.error("For 'String' or 'Values Only' types, the Unit field must be empty.")
                else:
                    save_row(index)  # Save if all checks pass
                    st.session_state.saved_rows.add(index)
        else:
            save_row(index)  # Save without additional checks if status is Not Fixed or other
            st.session_state.saved_rows.add(index)
            
     # Display summary of saved rows
    saved_count = len(st.session_state.saved_rows)
    total_rows = len(st.session_state.input_data)
    st.markdown(f"### Progress: {saved_count} of {total_rows} rows saved")
    
    # Optionally, list saved row indices for quick reference
    st.write(f"Rows saved: {sorted(st.session_state.saved_rows)}")   
 
    # Add a search bar in the sidebar
    with st.sidebar:
        st.markdown("### Find Anything")
        search_query = st.text_input("Search", placeholder="Enter keyword or phrase")
        search_button = st.button("Find")
    
    # Function to perform the search
    def search_data(query, dataframe):
        if query:
            # Convert query to lowercase for case-insensitive matching
            query = query.lower()
            # Filter rows containing the query in any column
            filtered_data = dataframe[
                dataframe.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
            ]
            return filtered_data
        return pd.DataFrame()  # Return an empty DataFrame if query is empty
    
    # Perform the search if the button is clicked
    if search_button and search_query:
        results = search_data(search_query, input_data)  # Replace `df` with your DataFrame
        if not results.empty:
            st.markdown(f"### Search Results for '{search_query}'")
            st.dataframe(results)  # Display results in the main content area
        else:
            st.warning("No results found.")
       
        
        # Function to translate text=   
    @st.cache_data
    def translate_text(text):
        if pd.isnull(text):
            return ""
        try:
            return translator.translate(text, src='auto', dest='en').text
        except Exception as e:
            return text
    
    # Function to determine the correct domain based on the marketplace
    def get_amazon_domain(marketplace):
        if marketplace == "US":
            return "amazon.com"
        elif marketplace == "JP":
            return "amazon.co.jp"
        elif marketplace == "UK":
            return "amazon.co.uk"
        elif marketplace in ["BR", "MX", "AU", "TR", "BE", "CO", "NG"]:
            return f"amazon.com.{marketplace.lower()}"
        else:
            return f"www.amazon.{marketplace.lower()}"
    
    # Function to create a hyperlink for each ASIN based on the marketplace
    def create_hyperlink(asin, marketplace):
        domain = get_amazon_domain(marketplace)
        url = f"https://{domain}/dp/{asin}"
        return f'<a href="{url}" target="_blank">{asin}</a>'
    
    
    def main():
        
        # Display 500 rows per page
        rows_per_page = 500
        current_page = st.session_state.get('current_page', 0)
    
        # Calculate the starting and ending indices for the current page
        start_index = current_page * rows_per_page
        end_index = min(start_index + rows_per_page, len(input_data))
    
        for i in range(start_index, end_index):
            render_row(i)
            st.markdown("---")
    

        st.markdown("---")
        download_updated_file()
            
    # Call the main function
    if __name__ == "__main__":
        main()
else:
    st.warning("Please upload an input Excel file to proceed.") 

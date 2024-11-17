import streamlit as st
import time
import logging
from utils import setup_logging, get_completion, parse_yaml_response, display_explanation
from pathlib import Path
from docx import Document
import base64
from PIL import Image

logger = logging.getLogger(__name__)

def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="Simplify It",
        page_icon="💡",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        /* Global styles */
        .block-container {
            padding-top: 5rem !important;
            max-width: 1000px !important;
        }
        
        /* Header section */
        .header-container {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0 !important;
        }
        
        .header-title {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 3.5rem !important;
            font-weight: 700;
            color: #1E1E1E;
            margin: 0;
            line-height: 1.2;
        }
        
        .header-emoji {
            font-size: 3rem;
        }
        
        /* Subtitle */
        .subtitle {
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 1.5rem;
            color: #666;
            margin-top: 0;
            margin-bottom: 3rem;
            line-height: 1.5;
        }
        
        /* Updated input field style */
        .stTextInput > div > div > input {
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-size: 1rem !important;
            padding: 1.5rem !important;
            min-height: 3.5rem !important;
            border-radius: 8px !important;
            border: 2px solid #eee !important;
            transition: all 0.3s ease !important;
            line-height: 1.5 !important;
            box-sizing: border-box !important;
        }
        
        /* Ensure the container also respects the height */
        .stTextInput > div > div {
            min-height: 3.5rem !important;
        }
        
        .stTextInput > div {
            min-height: 3.5rem !important;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    
    # Custom header with logo and title
    st.markdown("""
        <div class="header-container">
            <div class="header-emoji">💡</div>
            <h1 class="header-title">Simplify It</h1>
        </div>
        <p class="subtitle">Let's make the world more simple.</p>
    """, unsafe_allow_html=True)

def display_document(doc_path: str):
    """Display the generated document content."""
    doc = Document(doc_path)
    
    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            st.header(paragraph.text)
        else:
            st.write(paragraph.text)

def display_images(images_folder: str):
    """Display the generated images in a grid."""
    try:
        image_files = sorted(Path(images_folder).glob("*.png"))
        image_files = list(image_files)  # Convert generator to list
        
        if not image_files:
            logger.warning(f"No images found in folder: {images_folder}")
            st.warning("No images available to display.")
            return
        
        # Create columns for images (max 3 per row)
        num_cols = min(len(image_files), 3)  # Limit to 3 columns max
        cols = st.columns(num_cols)
        
        # Display images in columns
        for idx, img_path in enumerate(image_files):
            col_idx = idx % num_cols  # Cycle through columns
            with cols[col_idx]:
                try:
                    image = Image.open(img_path)
                    st.image(
                        image, 
                        caption=f"Step {idx + 1}", 
                        use_container_width=True
                    )
                except Exception as e:
                    logger.error(f"Error displaying image {img_path}: {e}")
                    st.error(f"Failed to load image for Step {idx + 1}")
                    
    except Exception as e:
        logger.error(f"Error in display_images: {e}")
        st.error("Failed to display images.")

def main():
    setup_page()
    setup_logging()
    
    # Add custom styled header for the question
    st.markdown("""
        <h2 style="
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 2rem;
            font-weight: 500;
            color: #333;
            margin-bottom: 0;
            margin-top: 2rem;
        ">
            What would you like to learn about?
        </h2>
    """, unsafe_allow_html=True)
    
    # Input field without label
    user_intent = st.text_input(
        label="",  # Remove default label since we're using custom header
        placeholder="Enter a concept (e.g., 'quantum computing', 'blockchain', 'photosynthesis')",
        key="concept_input"
    )
    
    if user_intent:
        with st.spinner("Generating explanation..."):
            try:
                start_time = time.time()
                yaml_response = get_completion(user_intent)
                parsed_response = parse_yaml_response(yaml_response)
                
                if isinstance(parsed_response, dict):
                    output_folder = display_explanation(parsed_response, user_intent)
                    logger.info(f"Output folder: {output_folder}")
                    
                    # Display content
                    st.success(f"Generated explanation in {time.time() - start_time:.2f} seconds!")
                    
                    # Show title and introduction
                    st.title(parsed_response['title'])
                    st.write(parsed_response['introduction'])
                    
                    # Get images folder path
                    images_folder = output_folder.replace("output", "images")
                    logger.info(f"Looking for images in: {images_folder}")
                    
                    # Display steps with their corresponding images
                    for step in parsed_response['steps']:
                        st.header(f"{step['heading']}")
                        
                        # Display step text
                        st.write(step['text'])
                        
                        # Display corresponding image
                        image_path = Path(images_folder) / f"step_{step['step_number']}.png"
                        if image_path.exists():
                            try:
                                image = Image.open(image_path)
                                st.image(
                                    image,
                                    caption=step['image_description'],
                                    use_container_width=True,
                                )
                            except Exception as e:
                                logger.error(f"Error displaying image {image_path}: {e}")
                                st.error(f"Failed to load image for Step {step['step_number']}")
                        
                        # Display transition if exists
                        if 'transition' in step:
                            st.write(f"**Next:** {step['transition']}")
                    
                    # Display conclusion
                    st.header("Conclusion")
                    st.write(parsed_response['conclusion'])
                    
                    # Add download button for the document
                    doc_path = list(Path(output_folder).glob("*.docx"))[0]
                    with open(doc_path, "rb") as file:
                        btn = st.download_button(
                            label="📄 Download Document",
                            data=file,
                            file_name=f"{user_intent}_explanation.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                
                else:
                    st.error("Failed to generate explanation. Please try again.")
                    logger.error(f"Failed to parse YAML response: {yaml_response}")
            
            except Exception as e:
                st.error("An error occurred while generating the explanation.")
                logger.error(f"Error in Streamlit app: {e}", exc_info=True)

if __name__ == "__main__":
    main() 
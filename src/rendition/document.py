from docx import Document
import streamlit as st
from pathlib import Path
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def render_document(doc_path: str):
    """Render the document content."""
    doc = Document(doc_path)
    
    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            st.header(paragraph.text)
        else:
            st.write(paragraph.text)

def render_images_grid(images_folder: str):
    """Render images in a grid layout."""
    try:
        image_files = sorted(Path(images_folder).glob("*.png"))
        image_files = list(image_files)
        
        if not image_files:
            logger.warning(f"No images found in folder: {images_folder}")
            st.warning("No images available to display.")
            return
        
        num_cols = min(len(image_files), 3)
        cols = st.columns(num_cols)
        
        for idx, img_path in enumerate(image_files):
            col_idx = idx % num_cols
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
        logger.error(f"Error in render_images_grid: {e}")
        st.error("Failed to display images.") 
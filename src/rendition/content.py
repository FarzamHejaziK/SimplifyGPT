import streamlit as st
from pathlib import Path
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def render_input_section():
    """Render the user input section."""
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
    
    return st.text_input(
        label="",
        placeholder="Enter a concept (e.g., 'quantum computing', 'blockchain', 'photosynthesis')",
        key="concept_input"
    )

def render_explanation(parsed_response: dict, output_folder: str):
    """Render the explanation content."""
    # Create an anchor div at the top of the explanation
    st.markdown('<div id="explanation-start"></div>', unsafe_allow_html=True)
    
    st.title(parsed_response['title'])
    st.write(parsed_response['introduction'])
    
    images_folder = output_folder.replace("output", "images")
    logger.info(f"Looking for images in: {images_folder}")
    
    _render_steps(parsed_response['steps'], images_folder)
    _render_conclusion(parsed_response['conclusion'])
    _render_download_button(output_folder)

    # Add JavaScript to scroll to the anchor
    js = """
        <script>
            // Wait for the content to load
            setTimeout(function() {
                // Find the explanation start div
                const element = window.parent.document.querySelector('#explanation-start');
                // Scroll to it
                if (element) {
                    element.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }, 100);  // Small delay to ensure content is rendered
        </script>
    """
    st.markdown(js, unsafe_allow_html=True)

def _render_steps(steps: list, images_folder: str):
    """Render the explanation steps with images."""
    for step in steps:
        st.header(f"{step['heading']}")
        st.write(step['text'])
        
        image_path = Path(images_folder) / f"step_{step['step_number']}.png"
        if image_path.exists():
            try:
                image = Image.open(image_path)
                st.write(step['image_description'])
                st.image(image, use_container_width=True)
            except Exception as e:
                logger.error(f"Error displaying image {image_path}: {e}")
                st.error(f"Failed to load image for Step {step['step_number']}")
        
        if 'transition' in step:
            st.write(f"{step['transition']}")

def _render_conclusion(conclusion: str):
    """Render the conclusion section."""
    st.header("Conclusion")
    st.write(conclusion)

def _render_download_button(output_folder: str):
    """Render the document download button."""
    doc_path = list(Path(output_folder).glob("*.docx"))[0]
    with open(doc_path, "rb") as file:
        st.download_button(
            label="📄 Download Document",
            data=file,
            file_name=f"explanation.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ) 
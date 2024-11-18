import streamlit as st

def render_page_config():
    """Configure the Streamlit page layout and styling."""
    st.set_page_config(
        page_title="Simplify It",
        page_icon="💡",
        layout="wide"
    )
    
    _render_custom_styles()
    _render_header()

def _render_custom_styles():
    """Render custom CSS styles."""
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

def _render_header():
    """Render the page header."""
    st.markdown("""
        <div class="header-container">
            <div class="header-emoji">💡</div>
            <h1 class="header-title">Simplify It</h1>
        </div>
        <p class="subtitle">Let's make the world more simple.</p>
    """, unsafe_allow_html=True) 
import sys
import os
import io
from PIL import Image

# Add root to path
sys.path.append(os.getcwd())

# Mock the Groq API key if not present for testing logic flow
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = "mock_key"

def test_vision_flow():
    print("Testing Vision Service Flow...")
    
    # Create a dummy image (100x100 white square)
    img = Image.new('RGB', (100, 100), color = 'white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    # Import service (delayed import to ensure env vars are set)
    try:
        from backend.services.vision_service import analyze_image
        from backend.vision.inference import vision_service as local_vision
        
        # Checking if local vision service is initialized
        print(f"Local Vision Model Enabled: {local_vision.model is not None}")
        
        # Since we don't want to actually hit Groq API with a mock key (it will 401),
        # we are primarily testing that the code *reaches* the API call point 
        # after running the local inference.
        
        # We can inspect the local_vision.predict_image output
        pred = local_vision.predict_image(img_bytes)
        print(f"Prediction for dummy image: {pred}")
        
        if "label" in pred:
            print("SUCCESS: Local inference pipeline is working.")
        else:
            print("FAILURE: Local inference did not return a label.")
            
    except ImportError as e:
        print(f"Import Error: {e}")
    except Exception as e:
        print(f"Runtime Error: {e}")

if __name__ == "__main__":
    test_vision_flow()

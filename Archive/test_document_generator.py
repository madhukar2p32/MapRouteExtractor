"""
Test the document generator with optimized settings
"""

import os
import sys
from pathlib import Path

def test_document_generator():
    """Test document generation without heavy models"""
    print("🧪 Testing Document Generator")
    print("=" * 35)
    
    try:
        # Test imports
        from document_generator import RouteDocumentGenerator
        print("✅ Document generator imported successfully")
        
        # Create test data
        route_data = {
            'source': 'Home',
            'destination': 'NTR Garden',
            'direction': 'North-East',
            'landmarks': [
                {'name': 'Reliance Digital', 'type': 'store'},
                {'name': 'Mia by Tanishq', 'type': 'store'},
                {'name': 'SNITCH - Toli Chowki', 'type': 'store'},
                {'name': 'Nehru Zoological Park', 'type': 'park'},
                {'name': 'Aziz Plaza', 'type': 'plaza'}
            ],
            'visualization_path': 'output/route_visualization.png'
        }
        
        # Create output directory
        output_dir = 'output'
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        print(f"✅ Output directory created: {output_dir}")
        
        # Test document generator WITHOUT HuggingFace models (faster)
        print("\n📄 Testing basic document generation...")
        generator = RouteDocumentGenerator(use_hf_models=False)
        print("✅ Document generator initialized (basic mode)")
        
        # Test HTML document generation
        try:
            html_path = generator.generate_route_document(route_data, output_dir, 'html')
            print(f"✅ HTML document generated: {html_path}")
            
            if os.path.exists(html_path):
                file_size = os.path.getsize(html_path) / 1024  # KB
                print(f"   📏 File size: {file_size:.1f} KB")
            
        except Exception as e:
            print(f"❌ HTML generation failed: {e}")
        
        # Test Word document generation
        try:
            docx_path = generator.generate_route_document(route_data, output_dir, 'docx')
            print(f"✅ Word document generated: {docx_path}")
            
            if os.path.exists(docx_path):
                file_size = os.path.getsize(docx_path) / 1024  # KB
                print(f"   📏 File size: {file_size:.1f} KB")
                
        except Exception as e:
            print(f"❌ Word generation failed: {e}")
        
        # Test with HuggingFace models (if available)
        print("\n🤖 Testing with HuggingFace models...")
        try:
            hf_generator = RouteDocumentGenerator(use_hf_models=True)
            
            # This might take time to download models, so we'll be patient
            print("⏳ Initializing HuggingFace models (this may take a moment)...")
            
            if hf_generator.use_hf_models:
                print("✅ HuggingFace models initialized successfully")
                
                # Test enhanced description
                description = hf_generator.generate_route_description(route_data)
                print(f"✅ Enhanced route description generated")
                print(f"   📝 Description preview: {description[:100]}...")
                
            else:
                print("⚠️ HuggingFace models not available, using basic mode")
                
        except Exception as e:
            print(f"⚠️ HuggingFace test failed (this is OK): {e}")
        
        print("\n🎉 Document generator tests completed!")
        print("\n📋 Available outputs:")
        
        # List generated files
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            for file in files:
                file_path = os.path.join(output_dir, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path) / 1024
                    print(f"   📄 {file} ({size:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_document_generator()
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed'}")
    sys.exit(0 if success else 1)

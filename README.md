# 🧭 Map Route Extractor & Documentation System

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3+-green.svg)
![OpenCV](https://img.shields.io/badge/opencv-v4.8+-orange.svg)
![HuggingFace](https://img.shields.io/badge/huggingface-transformers-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A comprehensive AI-powered solution for extracting routes from map images and generating professional documentation using HuggingFace models and computer vision.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/map-route-extractor.git
cd map-route-extractor

# Install dependencies
pip install -r requirements.txt

# Run the application
python launch_app.py
```

Visit `http://localhost:5000` and start extracting routes!

## ✨ Features

### 🎯 Core Capabilities
- **🖼️ Smart Image Processing**: Advanced blue route line detection using OpenCV
- **📍 Intelligent Labeling**: Automatic source/destination identification with spatial logic
- **🧭 Compass Integration**: Direction indicators with N/E/S/W markers
- **🏛️ Landmark Detection**: AI-powered identification of schools 🏫, hospitals 🏥, temples 🛕
- **📄 Professional Documentation**: Word document generation with enhanced formatting
- **🌐 Modern Web Interface**: Responsive design with drag-and-drop functionality

### 🤖 AI Integration
- **HuggingFace Models**: GPT-2 for text generation, BART for summarization
- **Computer Vision**: HSV color space optimization for precise route detection
- **Natural Language Processing**: Automated route descriptions and documentation
- **Smart Fallbacks**: Graceful degradation when AI models unavailable

### 📊 Advanced Processing
- **Morphological Operations**: Noise reduction and route refinement
- **Contour Analysis**: Intelligent scoring system for route selection
- **Spatial Positioning**: Logic-based endpoint labeling (top-left → bottom-right)
- **Dual Extraction**: Basic and enhanced processing modes

## 🖥️ Screenshots

### Web Interface
![Web Interface](docs/images/web-interface.png)

### Route Extraction
![Route Extraction](docs/images/route-extraction.png)

### Generated Documentation
![Documentation](docs/images/documentation.png)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   AI Processing │    │   Document Gen  │
│   (Flask + JS)  │───▶│   (OpenCV + HF) │───▶│   (python-docx) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   File Upload   │    │   Route         │    │   Multi-format  │
│   & Validation  │    │   Extraction    │    │   Export        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB+ RAM (for AI models)

### Step-by-Step Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/map-route-extractor.git
   cd map-route-extractor
   ```

2. **Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python launch_app.py
   ```

5. **Access Web Interface**
   - Open browser to `http://localhost:5000`
   - Upload map image with blue route
   - Generate professional documentation

## 📋 Usage

### Web Interface
1. **Upload Image**: Drag & drop or click to select map image
2. **Set Locations**: Enter source and destination names
3. **Extract Route**: Click "Extract Route & Generate Document"
4. **Download Results**: Get PNG visualization and Word document

### Programmatic Usage
```python
from simple_converter import extract_blue_lines_with_labels, create_enhanced_word_document_with_labels

# Extract route with labels
image_path, landmarks = extract_blue_lines_with_labels(
    "input_map.jpg", 
    "output_route.png",
    source_name="Home",
    destination_name="Office"
)

# Generate documentation
doc_path = create_enhanced_word_document_with_labels(
    landmarks, 
    "route_document.docx",
    source_name="Home",
    destination_name="Office"
)
```

### API Usage
```python
import requests

response = requests.post('http://localhost:5000/api/process', {
    'source': 'Home',
    'destination': 'Work',
    'image': 'base64_encoded_image'
})
```

## ⚙️ Configuration

### Core Settings (`config.json`)
```json
{
  "blue_color_range": {
    "lower": [100, 80, 80],
    "upper": [130, 255, 255]
  },
  "huggingface_models": {
    "text_generation": "gpt2",
    "summarization": "facebook/bart-large-cnn"
  },
  "landmark_detection": {
    "enabled": true,
    "max_landmarks": 10
  }
}
```

### Environment Variables
```bash
export HUGGINGFACE_HUB_TOKEN=your_token_here
export FLASK_ENV=production
export MAX_CONTENT_LENGTH=16777216
```

## 🧪 Testing

### Run All Tests
```bash
python test_system.py
```

### Test Components
```bash
python test_components.py          # Core functionality
python test_enhanced_features.py   # Enhanced features  
python test_document_generator.py  # Document generation
python test_web_compatibility.py   # Web interface
```

### Test Coverage
- ✅ Route extraction algorithms
- ✅ Document generation
- ✅ Web interface functionality
- ✅ AI model integration
- ✅ Error handling and fallbacks

## 🚀 Deployment

### Local Development
```bash
python launch_app.py
```

### Production Deployment
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "launch_app.py"]
```

### Cloud Deployment
- **Heroku**: Ready for deployment
- **AWS**: EC2 or Lambda support
- **Google Cloud**: App Engine compatible
- **Azure**: Web Apps ready

## 📊 Performance

### Benchmarks
- **Route Extraction**: ~2-5 seconds per image
- **Document Generation**: ~1-3 seconds
- **AI Text Generation**: ~3-8 seconds (first run)
- **Total Processing**: ~5-15 seconds per route

### Resource Usage
- **CPU**: 2-4 cores recommended
- **RAM**: 4-8GB (including AI models)
- **Storage**: 2-5GB (models + cache)
- **Network**: Required for initial model download

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contributing Steps
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

### Areas for Contribution
- 🔍 Algorithm improvements
- 🎨 UI/UX enhancements
- 📝 Documentation updates
- 🧪 Test coverage expansion
- 🌐 Internationalization
- 📱 Mobile app development

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

### Version 2.1 (Planned)
- [ ] Advanced OCR integration
- [ ] Multi-language support
- [ ] Batch processing
- [ ] API authentication

### Version 3.0 (Future)
- [ ] Mobile applications
- [ ] Real-time processing
- [ ] Cloud deployment
- [ ] Advanced AI models

## 🆘 Support

### Documentation
- [Installation Guide](docs/installation.md)
- [API Reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

### Community
- **Issues**: [GitHub Issues](https://github.com/yourusername/map-route-extractor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/map-route-extractor/discussions)
- **Wiki**: [Project Wiki](https://github.com/yourusername/map-route-extractor/wiki)

### Contact
- **Email**: [support@your-domain.com]
- **Twitter**: [@YourHandle]
- **LinkedIn**: [Your Profile]

## 🙏 Acknowledgments

### Technologies Used
- **OpenCV**: Computer vision processing
- **HuggingFace**: AI model integration
- **Flask**: Web framework
- **python-docx**: Document generation

### Contributors
- **Core Development**: [Your Name]
- **UI/UX Design**: [Designer Name]
- **Testing**: [Tester Name]
- **Documentation**: [Writer Name]

### Special Thanks
- OpenCV community for excellent documentation
- HuggingFace team for accessible AI models
- Flask community for web framework
- All contributors and users

---

**⭐ Star this repository if you find it useful!**

**🔗 Share with others who might benefit from automated route extraction!**

**🤝 Contribute to make it even better!**

---

<div align="center">
  <sub>Built with ❤️ by developers, for developers</sub>
</div>

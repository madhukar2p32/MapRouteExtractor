# Contributing to Map Route Extractor

Thank you for your interest in contributing to the Map Route Extractor project! 🎉

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Flask, OpenCV, and HuggingFace

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/map-route-extractor.git
   cd map-route-extractor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**
   ```bash
   python test_system.py
   ```

## 🛠️ Development Workflow

### Branch Naming
- `feature/your-feature-name`
- `bugfix/issue-description`
- `enhancement/improvement-description`

### Commit Messages
Use conventional commits format:
- `feat: add new route detection algorithm`
- `fix: resolve source/destination labeling issue`
- `docs: update installation instructions`
- `test: add unit tests for document generator`

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python test_system.py

# Test specific components
python test_components.py
python test_document_generator.py
python test_enhanced_features.py
```

### Adding New Tests
- Place test files in the root directory with `test_` prefix
- Follow existing test patterns
- Test both success and failure scenarios

## 🐛 Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs
- Sample images (if applicable)

## 💡 Feature Requests

For new features, please:
- Check existing issues first
- Describe the problem it solves
- Provide implementation ideas
- Consider backward compatibility

## 📝 Code Style

### Python Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings for functions and classes
- Keep functions focused and small

### Documentation
- Update README.md for new features
- Add inline comments for complex logic
- Include examples in docstrings

## 🔄 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Write clean, tested code
   - Update documentation
   - Add/update tests

3. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Create Pull Request**
   - Use clear title and description
   - Reference related issues
   - Include screenshots if UI changes

### PR Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Performance impact considered

## 🏗️ Project Structure

```
MapRouteExtractor/
├── app.py                    # Flask web application
├── route_extractor.py        # Core route extraction logic
├── document_generator.py     # Document generation with HuggingFace
├── simple_converter.py       # Enhanced route processing
├── launch_app.py            # Application launcher
├── config.json              # Configuration settings
├── requirements.txt         # Python dependencies
├── templates/              # HTML templates
├── static/                # CSS, JS, images
├── tests/                 # Test files
└── docs/                  # Documentation
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Improve route detection accuracy
- [ ] Add more image format support
- [ ] Enhance landmark detection
- [ ] Mobile app development

### Medium Priority
- [ ] Add unit tests
- [ ] Improve error handling
- [ ] Performance optimization
- [ ] Multi-language support

### Low Priority
- [ ] UI/UX improvements
- [ ] Additional export formats
- [ ] API documentation
- [ ] Docker support

## 📚 Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [HuggingFace Documentation](https://huggingface.co/docs)

### Tools
- [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/)

## 🤝 Community

### Getting Help
- Create an issue for bugs or questions
- Join discussions in existing issues
- Check the README for setup instructions

### Code of Conduct
- Be respectful and inclusive
- Help others learn and grow
- Focus on constructive feedback
- Follow GitHub's community guidelines

## 🎉 Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Invited to the contributors team

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy coding! 🚀**

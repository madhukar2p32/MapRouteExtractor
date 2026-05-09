# 🔵 Blue Route Extractor - Extract Routes from Images

## 🎯 What This Does

This application **extracts existing blue lines** from your map images and creates clean Word documents with:
1. **Extracted blue route visualization** (white background, blue lines only)
2. **Source and destination** information
3. **Detected landmarks** along the route
4. **Minimal, clean formatting** - no extra explanations

## 🚀 How to Start

### **Easy Way: Double-Click**
1. Navigate to your MapRouteExtractor folder
2. **Double-click `start_simple_converter.bat`**
3. Wait for the server to start
4. Open browser to: **http://localhost:5001**

### **Command Line Way:**
```powershell
& "C:\Users\Madhukar K\Desktop\Python_Code\HuggingFace\venv\Scripts\python.exe" simple_converter.py
```

## 🌐 Using the Web Interface

1. **Upload Your Map Image**
   - Click upload area or drag & drop your image
   - Must contain blue route lines
   - Supports: PNG, JPG, JPEG, BMP, GIF

2. **Enter Route Information**
   - Source: Starting point name
   - Destination: End point name

3. **Automatic Processing**
   - Detects blue color ranges in HSV
   - Extracts only blue route structures
   - Creates white background with blue lines only
   - Identifies landmark points automatically

4. **Download Clean Document**
   - Word document with extracted blue route
   - Source → Destination title
   - Route visualization (blue on white)
   - Route details table
   - Detected landmarks list

## 📋 What You Get - Minimal & Clean

### **Word Document Contains ONLY:**
- **Title**: Source → Destination
- **Route Image**: Pure blue lines on white background
- **Route Details Table**: Source and Destination
- **Landmarks**: Auto-detected blue points with coordinates
- **No extra text, no explanations, no disclaimers**

### **Blue Route Extraction:**
- 🔍 **HSV Color Detection**: Identifies blue color ranges (HSV 100-130)
- 🧹 **Noise Cleaning**: Removes small artifacts
- ⚪ **White Background**: Clean visualization 
- 🔵 **Pure Blue Lines**: Only the route structure
- � **Landmark Detection**: Finds blue points and areas

## 🔧 Technical Processing

### **Image Processing:**
1. Convert BGR to HSV color space
2. Create mask for blue color range (100-130 hue)
3. Apply morphological operations to clean noise
4. Extract blue pixels to white background
5. Detect contours for landmark identification
6. Generate clean blue-on-white visualization

### **Document Generation:**
- Minimal Word document structure
- Route table with source/destination
- Blue route image embedded
- Landmark coordinates listed
- Clean, professional formatting

## 🔧 Technical Details

### **Runs on Port 5001**
- Different from the main app (port 5000)
- Can run simultaneously with the main app
- Lightweight and fast

### **Dependencies Used:**
- ✅ Flask (web interface)
- ✅ python-docx (Word document creation)
- ✅ OpenCV (image processing with blue lines)
- ✅ Pillow (image handling)

### **Automatic Features:**
- **Smart file naming** with timestamps
- **Error handling** for unsupported files
- **Automatic cleanup** of temporary files
- **Professional document formatting**

## 📁 File Structure

```
MapRouteExtractor/
├── simple_converter.py          # Main application
├── start_simple_converter.bat   # Easy launcher
├── templates/
│   └── simple_upload.html       # Upload interface
├── simple_uploads/              # Uploaded images
└── simple_output/               # Generated documents
```

## 🎨 Interface Features

### **Modern Design:**
- Beautiful gradient background
- Drag & drop file upload
- Real-time upload feedback
- Processing animations
- Professional styling

### **User Experience:**
- **Visual feedback** when files are selected
- **Progress indicators** during processing
- **Error messages** for invalid files
- **Automatic download** of Word documents

## 🔍 Example Workflow

1. **Start the app**: Double-click `start_simple_converter.bat`
2. **Open browser**: Go to http://localhost:5001
3. **Upload image**: Drag your map image to the upload area
4. **Click convert**: Press "Convert to Word Document"
5. **Download**: Word document downloads automatically
6. **Result**: Professional document with blue route line

## ✅ Ready to Use!

Your simple converter is ready! It provides exactly what you requested:
- ✅ Frontend for image upload
- ✅ Automatic blue line addition
- ✅ Word document generation
- ✅ Professional appearance
- ✅ Easy to use interface

## 🎉 Start Converting!

Run `start_simple_converter.bat` and begin converting your images to professional Word documents with blue route lines!

---
*Simple, focused, and efficient - exactly what you asked for!*

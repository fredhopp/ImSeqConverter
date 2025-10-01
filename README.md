# Image Sequence Converter

A professional-grade application for converting image sequences and video files with advanced color space management, designed specifically for VFX and post-production workflows.

![ImSeqConverter UI](docs/screenshot.png)

## Features

### Core Functionality
- **Image Sequence Detection** - Automatically detects and groups image sequences using intelligent file pattern recognition
- **Batch Processing** - Convert multiple sequences with individual settings
- **Drag & Drop Interface** - Modern, intuitive user interface
- **Video Input Support** - Convert existing video files (MOV, AVI, MKV, MP4)

### Professional Video Features
- **Multiple Output Formats**
  - MP4 with H.264/H.265 encoding
  - MOV with ProRes encoding
- **Color Space Management** - Professional color space conversion using LUTs
  - ACEScg, sRGB, Rec.709 workflows
  - Custom LUT support for any color space
- **Quality Presets** - High/Medium/Low quality settings
- **Resolution Options** - Original, 1080p, UHD (4K)
- **Frame Rate Control** - 23.976, 24, 25, 29.97, 30 fps

### Advanced Features
- **Frame Overlays** - Optional frame numbers and title overlays
- **Trim Functionality** - Head/tail frame trimming (up to 2000 frames)
- **Progress Tracking** - Real-time conversion progress with cancel support
- **Preferences System** - Configurable paths for FFmpeg, fonts, and LUTs

## Installation

### Prerequisites
- Windows 10/11
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z) (download and extract)
- Python 3.8+ (for development)

### Download
Download the latest release from the [Releases](https://github.com/fredhopp/ImSeqConverter/releases) page.

### Setup
1. Extract the application to your desired location
2. Run `ImSeqConverter.exe`
3. Configure preferences on first launch:
   - Set FFmpeg directory (path to bin folder)
   - Set font file path (TTF file for overlays)
   - Set LUT directory (color space conversion files)

## Usage

### Basic Workflow
1. **Add Files** - Click the "+" button or drag & drop image sequences/videos
2. **Configure Settings** - Select output format, color space, quality, etc.
3. **Set Output Path** - Choose destination folder
4. **Convert** - Click "Convert" to start batch processing

### Supported File Types
- **Image Sequences**: JPG, JPEG, PNG, TIF, TIFF, EXR, DPX, TGA
- **Video Files**: MOV, AVI, MKV, MP4

### Color Space Conversion
The application supports professional color space workflows:
- Configure LUT files in the preferences
- Select input and output color spaces from dropdown menus
- Automatic LUT application during conversion

## Development

### Project Structure
```
src/main/python/
├── main.py              # Application entry point
├── package/
│   ├── main_window.py   # Main UI implementation
│   ├── file_sequence.py # Sequence detection and parsing
│   ├── convert.py       # FFmpeg conversion logic
│   ├── worker.py        # Background processing
│   ├── preferences.py   # Settings management
│   └── luts.py          # Color space LUT handling
└── resources/           # Icons, fonts, LUTs, styles
```

### Building from Source
```bash
# Clone the repository
git clone https://github.com/fredhopp/ImSeqConverter.git
cd ImSeqConverter

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main/python/main.py

# Build executable with PyInstaller
pyinstaller main_onefile.spec
```

### Dependencies
- PySide6 (Qt for Python)
- clique (image sequence detection)
- FFmpeg (external dependency)

## Known Issues & Limitations

### Current Bugs
1. **File Names with Spaces** - Sequence parsing breaks if file names contain spaces (see `file_sequence.py:114`)
2. **Missing Error Handling** - Limited error handling for FFmpeg failures
3. **Progress Updates** - Progress dialog may not update properly during conversion

### Planned Improvements
- [ ] Fix file name parsing for spaces
- [ ] Add comprehensive error handling
- [ ] Improve progress tracking accuracy
- [ ] Add more output formats
- [ ] Implement preset saving/loading
- [ ] Add command-line interface

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for VFX and post-production workflows
- Uses FFmpeg for video processing
- Inspired by professional image sequence conversion needs

## Support

For issues, feature requests, or questions:
- Create an [Issue](https://github.com/fredhopp/ImSeqConverter/issues)
- Check existing documentation
- Review the code for technical details

---

**Note**: This application requires FFmpeg to be installed and configured. Make sure to set up your preferences correctly on first launch.
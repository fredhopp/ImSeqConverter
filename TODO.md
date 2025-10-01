# TODO List - Image Sequence Converter Project

## ✅ Completed Tasks

### Project Setup & Documentation
- [x] **Compare current local state with GitHub repository**
  - Local repo is on `dev` branch, up to date with `origin/dev`
  - Identified changes: modified files and untracked `_EXE/` directory

- [x] **Add _EXE directory to .gitignore**
  - Added `_EXE/` to prevent executable builds from being committed

- [x] **Assess current project state and identify potential bugs**
  - **Critical Bug**: File sequence parsing breaks if file names contain spaces (file_sequence.py:114)
  - **Medium Bug**: Limited error handling for FFmpeg failures
  - **Minor Bug**: Progress dialog updates may not be accurate

- [x] **Create SYSTEM_RULES.md with git push approval rule**
  - Added rule: NEVER push to GitHub unless explicitly approved by the user
  - Included development environment guidelines
  - Added project-specific rules for VFX workflows

- [x] **Create comprehensive README.md for GitHub**
  - Professional documentation with features, installation, and usage instructions
  - Detailed technical information about the application
  - Known issues section with identified bugs
  - Contributing guidelines and project structure

- [x] **Prepare first commit with clear message about project pickup**
  - All changes staged and ready
  - Commit message prepared
  - Waiting for user approval per SYSTEM_RULES.md

## 🎯 Current Status

### Ready for Commit
- **Files Staged**: `.gitignore`, `README.md`, `SYSTEM_RULES.md`, `file_sequence.py`, `main_window.py`
- **Commit Message**: "Project revival: First commit since picking up development again"
- **Status**: ⏳ **Waiting for user approval to push to GitHub**

## 🐛 Known Issues (To Fix Later)

### Critical Issues
- [ ] **Missing Last Frame Bug** - Frame range calculation loses the last frame
  - Location: `src/main/python/package/worker.py:24`
  - Formula: `framerange = end - start - (head + tail)` ❌ MISSING +1
  - Should be: `framerange = end - start + 1 - (head + tail)` ✅
  - Impact: Always loses the last frame of every sequence
  - Priority: **CRITICAL**

- [ ] **File Name Parsing Bug** - Sequence parsing breaks with spaces in file names
  - Location: `src/main/python/package/file_sequence.py:114`
  - Impact: Will cause index errors for sequences with spaces
  - Priority: High

### Medium Issues
- [ ] **Error Handling** - Limited error handling for FFmpeg failures
  - Need comprehensive error handling for subprocess calls
  - Should provide user-friendly error messages
  - Priority: Medium

### Minor Issues
- [ ] **Progress Updates** - Progress dialog may not update properly
  - Location: `src/main/python/package/main_window.py:347`
  - Impact: User experience during long conversions
  - Priority: Low

## ✅ Recently Completed (Latest)

### PyInstaller Configuration Fixes
- [x] **Fixed hardcoded paths in main_onefile.spec**
  - Removed `z:/Programming/ImSeqConverter` references
  - Updated to use relative paths: `src/main/python/main.py`
  - Location: `main_onefile.spec:7`

- [x] **Fixed hardcoded paths in constants.py**
  - Changed `Z:/Programming/ImSeqConverter/` to relative paths
  - Location: `src/main/python/package/constants.py:3-4`

- [x] **Added icon configuration to PyInstaller**
  - Icon file: `src/main/resources/icons/ImSeqConverter.ico` ✅ EXISTS
  - Added to spec: `icon='src/main/resources/icons/ImSeqConverter.ico'`
  - Location: `main_onefile.spec:37`

- [x] **Improved PyInstaller configuration**
  - Added resources: `datas=[('src/main/resources', 'resources')]`
  - Added hidden imports: PySide6 modules and clique
  - Set console=False for proper GUI app
  - Updated executable name to 'ImSeqConverter'

## 🔄 Next Steps

### Immediate (After User Approval)
1. Execute commit with PyInstaller fixes
2. Push changes to GitHub repository
3. Verify all changes are properly uploaded

### Current Development Tasks
1. **Test latest built executable** - Verify v1.1.0 build works correctly
2. **Fix preferences window behavior** - Bring to front when auto-opens on first start
3. **Improve marked files behavior** - Change visual feedback when conversion completed
4. **Add debug command line arguments** - Enable debug mode via CLI options
5. **Fix progress bars** - Make single and batch progress work as expected
6. **Show FFmpeg output** - Display FFmpeg execution in app terminal/console
7. **Commit and push improvements** - Save all changes to repository

### Future Development
1. Fix CRITICAL missing frame bug (worker.py:24) - frame range calculation
2. Fix file name parsing bug for spaces (file_sequence.py:114)
3. Implement comprehensive error handling
4. Add more output formats
5. Implement preset saving/loading
6. Add command-line interface

## 📝 Development Notes

### Recent Changes
- Increased trim head/tail range from 100 to 2000 frames
- Cleaned up commented code in main_window.py
- Added bug documentation comments
- Created professional documentation

### Project Structure
- Well-organized modular design
- Separate classes for conversion, file handling, preferences
- Worker thread for non-blocking UI
- Professional VFX workflow focus

---

**Last Updated**: Project revival commit preparation  
**Status**: Ready for user approval to push to GitHub

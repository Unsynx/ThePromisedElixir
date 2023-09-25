pyinstaller src/main.py --onefile --windowed --noconsole
cd dist
mkdir assets
cd ..
xcopy assets dist\assets /e

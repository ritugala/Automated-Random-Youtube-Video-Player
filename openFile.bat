cd C:\Users\Ritu\PycharmProjects\HIIT-Downloader
python extract_text.py
cd C:\Users\Ritu\Downloads\HIIT-Downloads
for /f %%i in ('dir /b/a-d/od/t:c') do set HIIT=%%i
%HIIT%
cd C:\Users\Ritu\PycharmProjects\HIIT-Downloader
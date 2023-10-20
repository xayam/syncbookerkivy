
.\venv\Scripts\pyan3 *.py --uses --no-defines --colored --grouped --annotated --svg > app_level1.svg

.\venv\Scripts\pyan3 src/*.py --uses --no-defines --colored --grouped --annotated --svg > app_level2.svg

.\venv\Scripts\pyan3 src/**/*.py --uses --no-defines --colored --grouped --annotated --svg > app_level3.svg

.\venv\Scripts\pyan3 src/**/**/*.py --uses --no-defines --colored --grouped --annotated --svg > app_level4.svg

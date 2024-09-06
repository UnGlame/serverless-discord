#!/bin/sh
echo "Zipping packages and source files into zip..."

PACKAGES_DIR="venv/lib/python3.12/site-packages"
ZIP_FILE="lambda_deployment_package.zip"
SOURCE_FILE="lambda_function.py"

if [ -f ZIP_FILE]; then
    echo "Deleting existing zip file..."
    rm ZIP_FILE
fi

# Zip packages into zip file
cd ${PACKAGES_DIR}
zip -r ../../../../${ZIP_FILE} .

# Add source file into zip
cd ../../../..
zip ${ZIP_FILE} ${SOURCE_FILE}

# Deploy to lambda
echo "Deploying to lambda..."
aws lambda update-function-code --function-name discord-interaction --zip-file fileb://lambda_deployment_package.zip

echo "Done."

FROM python:3.11-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1) \
    && wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION.0.0.0/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip || \
    wget -q "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION" -O /tmp/chrome_version.txt \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ || true \
    && chmod +x /usr/local/bin/chromedriver-linux64/chromedriver || true

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["pytest", "test_ecommerce.py", "-v", "--html=report.html", "--self-contained-html"]

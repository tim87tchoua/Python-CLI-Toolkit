# 🔧 Python CLI Toolkit

A small collection of command-line tools built with Python. Each script is self-contained and easy to use for learning, portfolio, or utility purposes.

## 🚀 Tools Included

1. **Password Generator** – Create strong, random passwords
2. **IP Lookup** – Get geolocation and details of any IP using ipinfo.io
3. **Ping Sweeper** – Scan a subnet to find online devices
4. **File Hasher** – Generate a SHA256 hash of any file
5. **Webpage Creator** – Generate a modern static landing page in seconds with sections for features, testimonials, pricing, and contact form

## 📦 Usage

```bash
python3 password_generator.py
python3 ip_lookup.py
python3 ping_sweeper.py
python3 file_hasher.py
python3 webpage_creator.py --title "My Brand" --subtitle "Modern digital solutions" --output-dir website
```

### Webpage Creator examples

```bash
python3 webpage_creator.py --title "GreenSpace" --subtitle "Sustainable home services" --description "Helping homeowners live greener." --feature "Eco:Eco-friendly solutions" --feature "Fast:Fast turnaround" --dark-mode --output-dir website
```

You can also add a contact email and custom CTA:

```bash
python3 webpage_creator.py --title "Launch Your Brand" --subtitle "A modern company landing page built in minutes." --button-text "Book a demo" --theme-color "#14b8a6" --dark-mode --contact-email "hello@launchyourbrand.com" --output-dir website
```

Open the generated `website/index.html` file in a browser to preview the page.

## ✅ Dependencies

Only `requests` is required (for ip_lookup). Install with:

```bash
pip install requests
```

Happy hacking 💻
# Python-CLI-Toolkit

🎨 AdNova-Studio

AdNova-Studio is an AI-powered Streamlit application that helps you generate high-quality product advertisements from text prompts or images using Bria AI APIs.

It enables creators, marketers, and developers to quickly produce studio-grade visuals, lifestyle shots, and ad creatives without manual design work.

🌟 Features
🖼️ Text-to-Image Generation
Generate high-quality product visuals from prompts
🏠 Lifestyle Shot Generation
Place products into realistic environments
🧩 Generative Fill
Modify or enhance parts of an existing image
🧼 Erase Elements
Remove unwanted objects or backgrounds
✨ Prompt Enhancement (AI-powered)
Automatically improve prompts for better outputs
🎯 Ad-Ready Outputs
Optimized for marketing and product showcase use-cases
🎮 Interactive UI (Streamlit)
Clean and intuitive user interface
💾 Download Generated Images
🧠 How It Works

AdNova-Studio integrates with Bria AI APIs to perform:

Text → Image generation
Image → Image editing
Context-aware image enhancement

The app processes user input and sends optimized requests to Bria APIs, returning production-quality visuals.

📦 Project Structure
AdNova-Studio/
│
├── components/        # UI components
├── services/          # API logic (Bria integration)
│   ├── hd_image_generation.py
│   ├── lifestyle_shot.py
│   ├── generative_fill.py
│   ├── erase_foreground.py
│
├── utils/             # Helper functions
├── workflows/         # Processing pipelines
├── app.py             # Main Streamlit app
├── .env               # API keys
├── requirements.txt
└── README.md

📁 Local folder name

The project directory should be **`AdNova-Studio`**. If yours is still **`AdNova-APP`**, close Cursor/VS Code and any terminals using that folder, then rename it:

`…\PROJECTS\AdNova-APP` → `…\PROJECTS\AdNova-Studio`

Re-open the project from the new path. The included `venv` uses path-agnostic activation (`activate.bat` / `activate`), so it keeps working after the rename.

⚙️ Installation
1. Clone the repository
git clone https://github.com/yourusername/AdNova-Studio.git
cd adnova-studio
2. Create virtual environment
python -m venv venv
Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Setup environment variables

Create a .env file:

BRIA_API_KEY=your_api_key_here
5. Run the app
streamlit run app.py
💡 Usage Guide
🖼️ Generate Image
Enter a prompt
Click Generate Images

Example:

A luxury perfume bottle on a marble surface, soft lighting, high-end product photography
🏠 Lifestyle Shot
Upload product image
Provide environment description

Example:

Place the smartphone on a modern desk with a laptop and coffee, soft natural lighting
🧩 Generative Fill
Upload image
Describe modification

Example:

Replace background with a wooden desk and soft daylight
🧼 Erase Elements
Upload image
Remove unwanted parts

Example:

Remove background clutter and keep only the product
🎯 Best Prompt Practices

Use structured prompts:

[object] + [environment] + [lighting] + [style]

Example:

A smartwatch on a wooden table, natural sunlight, minimal aesthetic, product photography
⚠️ Notes & Limitations
Some advanced parameters (e.g. enhance_image, content_moderation)
may cause API errors depending on your Bria plan
Keep payload minimal for stable results
Always validate your API key
🔐 Security

⚠️ Never expose your API key publicly
If leaked, regenerate it immediately from the Bria dashboard

🤝 Contributing

Contributions are welcome!

Fork the repository
Create a branch
Make your changes
Submit a Pull Request
📄 License

This project is licensed under the MIT License

🙏 Acknowledgments
Bria AI for image generation APIs
Streamlit for the UI framework
🚀 Future Improvements
🎯 Auto ad copy + CTA generation
🖼️ Batch image generation
📱 Social media ad templates
💰 SaaS deployment
⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!
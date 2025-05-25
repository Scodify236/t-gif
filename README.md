# ⚡ Trishul-GIF Explorer

A sleek, modern GIF search and discovery application powered by the Tenor API. Built with vanilla HTML, CSS, and JavaScript for lightning-fast performance and seamless user experience.

## 🌟 Features

- **🔍 Smart Search**: Search through millions of GIFs with intelligent autocomplete suggestions
- **📱 Responsive Design**: Beautiful interface that works perfectly on all devices
- **🚀 Infinite Scroll**: Seamlessly load more GIFs as you scroll
- **💫 Trending GIFs**: Discover the latest trending GIFs on load
- **🎯 Modal Preview**: Full-screen GIF preview with sharing capabilities
- **📤 Easy Sharing**: Copy GIF URLs to clipboard or use native sharing
- **⚡ Fast Loading**: Optimized performance with smooth animations
- **🎨 Modern UI**: Clean, professional design with hover effects

## 🖥️ Demo

![Trishul-GIF Explorer Screenshot](screenshot.png)

*Live Demo: [Insert your live demo URL here]*

## 🚀 Quick Start

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for GIF loading

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/trishul-gif-explorer.git
   cd trishul-gif-explorer
   ```

2. **Open the application**
   ```bash
   # Simply open index.html in your browser
   open index.html
   # Or serve it with a local server
   python -m http.server 8000
   # Or use Live Server extension in VS Code
   ```

3. **Start exploring GIFs!**
   - The app will load trending GIFs automatically
   - Use the search bar to find specific GIFs
   - Click on any GIF to view it in full screen

## 🎯 Usage

### Searching GIFs
- Type in the search bar to get autocomplete suggestions
- Press Enter or click the search button to search
- Popular categories are suggested when the search bar is focused

### Viewing GIFs
- Click any GIF thumbnail to open it in full-screen modal
- Use the share button to copy the GIF URL to clipboard
- Click outside the modal or press ESC to close

### Infinite Scroll
- Scroll down to automatically load more GIFs
- No pagination needed - content loads seamlessly

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **API**: Tenor GIF API v2
- **Icons**: Font Awesome 6
- **Fonts**: Inter, system fonts fallback
- **Features**: 
  - CSS Grid for responsive layout
  - Flexbox for component alignment
  - CSS custom properties for theming
  - Modern JavaScript async/await
  - Web Share API integration

## 📁 Project Structure

```
trishul-gif-explorer/
├── index.html          # Main HTML file
├── README.md          # Project documentation
├── screenshot.png     # App screenshot
└── assets/           # Additional assets (if any)
    └── icons/        # Custom icons (if any)
```

## ⚙️ Configuration

### API Key Setup

The app uses the Tenor API. To use your own API key:

1. Get a free API key from [Tenor API](https://tenor.com/developer/keyregistration)
2. Replace the API key in the JavaScript section:
   ```javascript
   const TENOR_API_KEY = 'YOUR_API_KEY_HERE';
   ```

### Customization

You can customize the app by modifying CSS variables in the `:root` selector:

```css
:root {
    --primary-color: #2c3e50;      /* Main brand color */
    --secondary-color: #3498db;    /* Accent color */
    --accent-color: #e74c3c;       /* Error/warning color */
    --background-color: #f4f6f7;   /* Page background */
    --text-color: #2c3e50;         /* Text color */
}
```

## 🎨 Features in Detail

### Smart Search Suggestions
- Real-time search suggestions from Tenor API
- Popular categories displayed on focus
- Keyboard navigation support

### Responsive Grid Layout
- Auto-adjusting grid based on screen size
- Mobile-optimized with smaller grid items
- Smooth hover animations

### Modal System
- Full-screen GIF preview
- Share functionality with fallback for older browsers
- Click outside to close functionality

### Performance Optimizations
- Lazy loading for images
- Debounced search suggestions
- Efficient DOM manipulation
- CSS animations for smooth interactions

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow existing code style and conventions
- Test your changes across different browsers
- Add comments for complex functionality
- Update README.md if needed

## 🐛 Known Issues

- Some older browsers may not support the Web Share API (fallback to clipboard copy is provided)
- Very large GIFs may take time to load depending on internet connection


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Tenor API](https://tenor.com/developer) for providing the GIF database
- [Font Awesome](https://fontawesome.com/) for the beautiful icons
- [Google Fonts](https://fonts.google.com/) for the Inter font family

## 📞 Support

If you have any questions or need help:

- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/trishul-gif-explorer/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/trishul-gif-explorer/discussions)

## ⭐ Show Your Support

If you like this project, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with friends
- Contributing to make it better

---

**Built with ❤️ by Shashwat**

*Made possible by the amazing Tenor API and the open-source community.*

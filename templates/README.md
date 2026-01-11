# Templates Folder 📄

This folder contains the HTML templates for the Weather Chat Assistant application.

## Files

### `chat.html`
The main web interface for the weather chat application.

**Contains:**
- HTML structure
- CSS styling (embedded in `<style>` tags)
- JavaScript functionality (embedded in `<script>` tags)

**Features:**
- Responsive design
- Modern gradient UI
- Real-time weather queries
- Example query suggestions
- Dynamic result display

## Usage

Flask automatically loads templates from this folder using the `render_template()` function.

**In app.py:**
```python
from flask import render_template

@app.route('/chat')
def chat():
    return render_template('chat.html')
```

## Customization

### Change Colors
Edit the CSS section in `chat.html`:
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Modify Layout
Edit the HTML structure:
```html
<div class="container">
    <!-- Your changes here -->
</div>
```

### Update Behavior
Edit the JavaScript functions:
```javascript
async function submitQuery() {
    // Your changes here
}
```

## Best Practices

### Keep It Simple
- Single file for now (HTML + CSS + JS)
- Easy to maintain and deploy
- No build process needed

### Future Enhancements
If the project grows, consider splitting:
```
templates/
├── base.html          # Base layout
├── chat.html          # Extends base
└── components/
    ├── header.html
    └── footer.html

static/
├── css/
│   └── style.css
└── js/
    └── app.js
```

## Template Variables

Currently, `chat.html` doesn't use any Flask template variables (no `{{ }}` syntax).

If you want to pass data from Python to the template:

**In app.py:**
```python
@app.route('/chat')
def chat():
    return render_template('chat.html', 
                         app_name="Weather Chat",
                         version="1.0")
```

**In chat.html:**
```html
<h1>{{ app_name }}</h1>
<p>Version: {{ version }}</p>
```

## Important Notes

1. **This folder must exist** - Flask requires it
2. **File names matter** - Use exact names referenced in `render_template()`
3. **Relative paths** - Flask looks in this folder automatically
4. **Include in deployment** - Make sure this folder is in your Git repo

## Testing Changes

After editing `chat.html`:

1. Save the file
2. Refresh your browser (Ctrl+F5 to clear cache)
3. Changes should appear immediately
4. No need to restart Flask in debug mode

## Troubleshooting

### "Template not found" error
- Verify file exists: `templates/chat.html`
- Check file name spelling
- Ensure `templates/` folder is in the same directory as `app.py`

### Changes not showing
- Clear browser cache (Ctrl+F5)
- Check if editing the correct file
- Verify Flask is running in debug mode

### Styling issues
- Check browser console (F12) for errors
- Verify CSS syntax
- Test in different browsers

## Resources

- [Flask Templates Documentation](https://flask.palletsprojects.com/en/latest/tutorial/templates/)
- [Jinja2 Template Engine](https://jinja.palletsprojects.com/)
- [HTML/CSS/JS Reference](https://developer.mozilla.org/en-US/)

---

**Need help?** Check the main [README.md](../README.md) or [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)

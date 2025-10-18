# Chronos - The AI Archeologist

An automated text reconstruction application that uses AI and web search to expand slang, explain context, and provide relevant sources.

## Features

This application performs a fully automated four-step process:

1. **Get Input**: Accepts text with slang, abbreviations, and incomplete sentences
2. **Reconstruct with AI**: Uses Google Gemini API to expand slang and explain context
3. **Find Sources Online**: Performs web search to find relevant contextual sources
4. **Generate Report**: Creates a structured "Reconstruction Report" with all results

## Example

**Input**: `"lol, that was epic fail. brb"`

**Output**:
```
================================================================================
                    TEXT RECONSTRUCTION REPORT
================================================================================

1. ORIGINAL FRAGMENT:
   "lol, that was epic fail. brb"

2. AI-RECONSTRUCTED TEXT:
   "Laughing out loud, that was a significant and embarrassing mistake or failure. 
   Be right back."

3. CONTEXTUAL SOURCES:
   1. Epic Fail - Wikipedia
      Link: https://en.wikipedia.org/wiki/Epic_fail
      Summary: Epic fail is an internet slang expression used to describe...

   2. Internet Slang Dictionary - LOL, BRB
      Link: https://www.internetslang.com/
      Summary: Comprehensive dictionary of internet slang including LOL, BRB...
```

## Quick Start

### Option 1: VS Code (Recommended)
1. Open VS Code
2. File → Open Folder → Select this `text-reconstruction-app` folder
3. Open the integrated terminal (Terminal → New Terminal)
4. Run: `/usr/bin/python3 text_reconstruction_app.py`

### Option 2: Command Line
1. Navigate to the project folder:
   ```bash
   cd text-reconstruction-app
   ```
2. Run the application:
   ```bash
   /usr/bin/python3 text_reconstruction_app.py
   ```

## Setup Instructions

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Configure API Keys
The `.env` file is already configured with your API keys:
- ✅ Google Gemini API Key
- ✅ Google Custom Search API Key  
- ✅ Google Custom Search Engine ID

### 3. Run the Application
```bash
/usr/bin/python3 text_reconstruction_app.py
```

## File Structure

```
text-reconstruction-app/
├── text_reconstruction_app.py    # Main application
├── requirements.txt              # Python dependencies
├── .env                         # API keys (configured)
├── .env.example                 # API keys template
├── README.md                    # This documentation
├── demo.py                      # Demo script
├── test_app.py                  # Test script
└── text-reconstruction-app.code-workspace  # VS Code workspace
```

## Usage

1. Run the application
2. Enter your text when prompted (e.g., "lol, that was epic fail. brb")
3. The application will:
   - Process the text with AI
   - Search for relevant sources
   - Generate a comprehensive report
4. Optionally save the report to a file

## How It Works

### Step 1: Input Processing
- Validates and accepts user input text
- Handles various formats and lengths

### Step 2: AI Reconstruction
- Sends text to Google Gemini API
- Uses a specialized prompt to:
  - Expand slang and abbreviations
  - Explain colloquial expressions
  - Complete incomplete sentences
  - Maintain original tone and intent

### Step 3: Web Search
- Extracts key terms from reconstructed text
- Performs targeted web search using Google Custom Search API
- Retrieves top 5 most relevant sources

### Step 4: Report Generation
- Combines all results into a structured report
- Formats output for easy reading
- Includes timestamps and metadata

## VS Code Integration

This project includes a VS Code workspace file (`text-reconstruction-app.code-workspace`) with:
- Python interpreter configured to `/usr/bin/python3`
- Recommended Python extensions
- Proper file exclusions for Python cache files

To open in VS Code:
1. Open VS Code
2. File → Open Workspace from File
3. Select `text-reconstruction-app.code-workspace`

## API Usage and Costs

### Google Gemini API
- Free tier: 60 requests per minute
- Pricing: Check [Google AI pricing](https://ai.google.dev/pricing)

### Google Custom Search API
- Free tier: 100 search queries per day
- Pricing: $5 per 1000 queries after free tier

## Error Handling

The application includes comprehensive error handling for:
- Missing API keys
- Network connectivity issues
- API rate limiting
- Invalid input text
- Search API failures

## Customization

You can customize the application by modifying:
- `num_results` parameter in `search_contextual_sources()` for more/fewer search results
- The Gemini prompt in `reconstruct_text_with_ai()` for different reconstruction styles
- Report formatting in `generate_report()` for different output formats

## Requirements

- Python 3.9+ (system Python recommended)
- Internet connection
- Valid API keys for Google Gemini and Google Custom Search

## Troubleshooting

### Common Issues

1. **"API key not found" error**
   - Ensure your `.env` file exists and contains valid API keys
   - Check that the environment variable names match exactly

2. **"Search API quota exceeded" error**
   - You've hit the daily limit for Google Custom Search API
   - Wait 24 hours or upgrade to a paid plan

3. **"Gemini API error"**
   - Check your API key is valid and has sufficient quota
   - Ensure you have internet connectivity

### Getting Help

If you encounter issues:
1. Check the error message for specific details
2. Verify your API keys are correct and active
3. Ensure all dependencies are installed
4. Check your internet connection

## License

This project is open source and available under the MIT License.
# chronos
# chronos
# chronos
# chronos

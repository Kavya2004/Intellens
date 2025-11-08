# Setting up Gemini API (Free)

## Getting Your Free Gemini API Key

1. **Visit Google AI Studio**: Go to [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

2. **Sign in**: Use your Google account to sign in

3. **Create API Key**: Click "Create API Key" button

4. **Copy the Key**: Copy the generated API key

5. **Add to Environment**: 
   - Copy `.env.example` to `.env`
   - Replace `your_gemini_api_key_here` with your actual API key

## Free Tier Limits (Gemini 1.5 Flash)

- **15 requests per minute**
- **1 million tokens per minute** 
- **1,500 requests per day**
- **Free forever** - No credit card required

This is more than enough for analyzing most projects!

## Example .env file

```
GEMINI_API_KEY=AIzaSyD...your_actual_key_here
```

## Troubleshooting

If you get API errors:
1. Check that your API key is correct
2. Ensure you haven't exceeded rate limits
3. The system will fall back to static descriptions if API fails
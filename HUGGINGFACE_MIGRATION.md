# Migration to Hugging Face API

## Summary of Changes

This project has been updated to use **Hugging Face's free Inference API** instead of OpenAI's paid API. This makes the application more accessible while maintaining high-quality AI-powered resume optimization.

## What Changed?

### 1. AI Service (`backend/services/ai_optimizer.py`)
- ✅ Replaced OpenAI client with Hugging Face Inference API
- ✅ Uses `requests` library for HTTP API calls
- ✅ Default model: `mistralai/Mistral-7B-Instruct-v0.2`
- ✅ Maintains the same interface - no changes needed in other code
- ✅ Fallback to mock optimizer if no API key is provided

### 2. Configuration (`backend/core/config.py`)
- ✅ Removed `OPENAI_API_KEY` setting
- ✅ Added `HUGGINGFACE_API_KEY` setting
- ✅ Added `HUGGINGFACE_MODEL` setting (configurable)

### 3. Dependencies (`requirements.txt`)
- ❌ Removed `openai==1.3.7`
- ❌ Removed `anthropic==0.7.7`
- ❌ Removed `transformers==4.35.2` (not needed for API)
- ❌ Removed `torch==2.1.1` (not needed for API)
- ✅ Using existing `requests` library for API calls

### 4. Environment Files
- ✅ Created `env.example` with Hugging Face configuration
- ✅ Added detailed comments and model options

### 5. Documentation
- ✅ Updated `README.md`
- ✅ Updated `QUICKSTART.md`
- ✅ Updated `SETUP_GUIDE.md`
- ✅ Created `HUGGINGFACE_SETUP.md` (step-by-step guide)
- ✅ Created `HUGGINGFACE_MIGRATION.md` (this file)

## Benefits of Hugging Face

| Aspect | OpenAI (Before) | Hugging Face (Now) |
|--------|----------------|-------------------|
| **Cost** | $0.01-0.03 per request | **FREE** |
| **Setup** | Credit card required | No payment needed |
| **API Key** | Paid account needed | Free signup |
| **Rate Limits** | Based on payment tier | Generous free tier |
| **Models** | Proprietary (GPT-4) | Open source (Mistral, Llama) |
| **Quality** | Excellent | Very good |
| **Transparency** | Closed source | Open source |

## Available Models

The app now supports multiple Hugging Face models:

### Default Model (Recommended)
```env
HUGGINGFACE_MODEL="mistralai/Mistral-7B-Instruct-v0.2"
```
- Excellent quality
- Good speed
- Best balance for most users

### Alternative Models

```env
# Meta's Llama 2
HUGGINGFACE_MODEL="meta-llama/Llama-2-7b-chat-hf"

# Zephyr (faster)
HUGGINGFACE_MODEL="HuggingFaceH4/zephyr-7b-beta"

# Mixtral (most powerful, slower)
HUGGINGFACE_MODEL="mistralai/Mixtral-8x7B-Instruct-v0.1"

# Falcon
HUGGINGFACE_MODEL="tiiuae/falcon-7b-instruct"
```

## API Differences

### Request Format

**Before (OpenAI):**
```python
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7
)
result = response.choices[0].message.content
```

**After (Hugging Face):**
```python
payload = {
    "inputs": full_prompt,
    "parameters": {
        "max_new_tokens": 2000,
        "temperature": 0.7,
        "top_p": 0.95
    }
}
response = requests.post(api_url, headers=headers, json=payload)
result = response.json()[0]['generated_text']
```

### Prompt Format

Hugging Face models use instruction format:
```
<s>[INST] You are an expert...

{task instructions} [/INST]</s>
```

## Migration Steps for Users

### For New Users
1. Run `./setup.sh`
2. Get free API key from https://huggingface.co/settings/tokens
3. Add to `.env`: `HUGGINGFACE_API_KEY="hf_..."`
4. Start using the app!

### For Existing Users (Migrating from OpenAI)
1. Pull latest code
2. Update dependencies: `pip install -r requirements.txt`
3. Remove old environment variables:
   ```bash
   # Remove these from .env:
   # OPENAI_API_KEY
   # ANTHROPIC_API_KEY
   ```
4. Add new environment variables:
   ```bash
   # Add to .env:
   HUGGINGFACE_API_KEY="hf_your_token_here"
   HUGGINGFACE_MODEL="mistralai/Mistral-7B-Instruct-v0.2"
   ```
5. Restart the backend server

## Performance Considerations

### Response Times
- **First request**: 20-30 seconds (cold start - model loading)
- **Subsequent requests**: 2-5 seconds
- **With PRO tier**: < 1 second (no cold starts)

### Quality Comparison
- **OpenAI GPT-4**: Excellent (proprietary)
- **Mistral-7B**: Very good (open source)
- **Mixtral-8x7B**: Excellent (open source, larger model)

For most resume optimization tasks, the quality difference is minimal.

### Rate Limits
- **Free tier**: Thousands of requests/month
- **Rate limits**: Applied during high traffic
- **Solution**: Wait a few seconds between requests
- **Upgrade**: PRO tier ($9/month) for higher limits

## Code Changes Summary

### Files Modified
1. `backend/core/config.py` - Configuration settings
2. `backend/services/ai_optimizer.py` - Main AI service
3. `requirements.txt` - Dependencies
4. `README.md` - Documentation
5. `QUICKSTART.md` - Quick start guide
6. `SETUP_GUIDE.md` - Detailed setup

### Files Added
1. `env.example` - Environment template with Hugging Face
2. `HUGGINGFACE_SETUP.md` - Detailed API key guide
3. `HUGGINGFACE_MIGRATION.md` - This file

### Files Removed
None - backward compatible with graceful fallback

## Backward Compatibility

The app maintains backward compatibility:
- ✅ Works without API key (mock mode)
- ✅ Same API interface for frontend
- ✅ Same database schema
- ✅ Same user experience

## Testing

To test the migration:

1. **Without API key** (should use mock):
   ```bash
   # Don't set HUGGINGFACE_API_KEY
   ./start_backend.sh
   # Try optimizing a resume - should use mock optimizer
   ```

2. **With API key** (should use real AI):
   ```bash
   # Set HUGGINGFACE_API_KEY in .env
   ./start_backend.sh
   # Try optimizing a resume - should use Hugging Face API
   ```

3. **Check logs**:
   ```
   Look for:
   - "Warning: Hugging Face API key not set" (mock mode)
   - "Hugging Face API error" (API issues)
   - Success: No warnings, resume gets optimized
   ```

## Troubleshooting

### "Invalid API token"
- Check your API key format (should start with `hf_`)
- Regenerate token at https://huggingface.co/settings/tokens

### "Model is loading" (Cold start)
- Wait 20-30 seconds on first request
- Normal behavior for free tier
- Consider PRO tier for instant responses

### "Rate limit exceeded"
- Wait a few seconds between requests
- Check rate limits: https://huggingface.co/pricing
- Upgrade to PRO tier if needed

## Future Enhancements

Potential improvements:
- [ ] Model caching for faster responses
- [ ] Support for custom fine-tuned models
- [ ] A/B testing different models
- [ ] Local model inference option
- [ ] Batch processing for multiple resumes

## Support

- **Hugging Face Docs**: https://huggingface.co/docs/api-inference
- **Get API Key**: https://huggingface.co/settings/tokens
- **Model Hub**: https://huggingface.co/models
- **Community**: https://discuss.huggingface.co/

## Conclusion

The migration to Hugging Face makes this app:
- ✅ **Free to use** - no payment required
- ✅ **More accessible** - lower barrier to entry
- ✅ **Open source** - transparent AI models
- ✅ **High quality** - comparable results
- ✅ **Easy to setup** - simple API key generation

Enjoy your free AI-powered resume optimizer! 🚀



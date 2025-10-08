# How to Get Your FREE Hugging Face API Key

## Why Hugging Face?

Hugging Face provides **FREE access** to powerful AI models through their Inference API. Unlike OpenAI which requires payment, Hugging Face offers:

✅ **Free tier** with thousands of requests per month  
✅ **No credit card required**  
✅ **Access to powerful models** like Mistral-7B and Llama-2  
✅ **Simple API** similar to OpenAI  
✅ **Open-source models** - full transparency  

## Getting Your API Key (5 Minutes)

### Step 1: Create a Free Account

1. Go to [https://huggingface.co/join](https://huggingface.co/join)
2. Sign up with your email or GitHub account
3. Verify your email address

### Step 2: Generate Your API Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click the **"New token"** button
3. Give your token a name (e.g., "Resume Optimizer")
4. Select **"Read"** access (this is sufficient for the Inference API)
5. Click **"Generate token"**
6. **Copy the token** - it will look like: `hf_xxxxxxxxxxxxxxxxxxxxx`

### Step 3: Add the Token to Your Project

1. Open the `.env` file in the project root
2. Find the line: `HUGGINGFACE_API_KEY=""`
3. Paste your token: `HUGGINGFACE_API_KEY="hf_xxxxxxxxxxxxxxxxxxxxx"`
4. Save the file

**That's it!** Your app is now powered by AI 🎉

## Testing Your Setup

1. Start the backend server:
   ```bash
   ./start_backend.sh
   ```

2. Start the frontend:
   ```bash
   ./start_frontend.sh
   ```

3. Upload a resume and try optimizing it for a job

## Available Models

The app uses `mistralai/Mistral-7B-Instruct-v0.2` by default. You can change the model in `.env`:

### Recommended Models

| Model | Description | Best For |
|-------|-------------|----------|
| `mistralai/Mistral-7B-Instruct-v0.2` | Default, excellent balance | General use ⭐ |
| `meta-llama/Llama-2-7b-chat-hf` | Meta's Llama 2 | Conversational tasks |
| `HuggingFaceH4/zephyr-7b-beta` | Fast and efficient | Quick responses |
| `mistralai/Mixtral-8x7B-Instruct-v0.1` | Most powerful | Best quality (slower) |
| `tiiuae/falcon-7b-instruct` | Good alternative | Varied tasks |

To change the model, edit `.env`:
```env
HUGGINGFACE_MODEL="meta-llama/Llama-2-7b-chat-hf"
```

## Free Tier Limits

Hugging Face's free tier includes:

- ✅ **Thousands of requests per month**
- ✅ **Access to all public models**
- ✅ **No credit card required**
- ⏱️ Some cold start delays (model loading time)
- ⏱️ Rate limiting during high traffic

### If You Hit Rate Limits

If you see rate limit errors:
1. Wait a few seconds between requests
2. Consider upgrading to Hugging Face PRO ($9/month) for:
   - Faster inference (no cold starts)
   - Higher rate limits
   - Priority access

## Troubleshooting

### "Invalid API token"
- Make sure you copied the entire token (starts with `hf_`)
- Check for extra spaces in the `.env` file
- Regenerate the token if needed

### "Model is loading"
- First request may take 20-30 seconds (cold start)
- Subsequent requests will be faster
- This is normal for the free tier

### "Rate limit exceeded"
- Wait a few seconds between requests
- The free tier resets limits periodically
- Consider PRO tier for heavy usage

### "Model not found"
- Check the model name spelling in `.env`
- Some models may require special access
- Stick with the recommended models above

## Alternative: Use Without API Key

The app will work without an API key, but with limited features:
- ❌ No AI-powered optimization
- ✅ Basic keyword matching still works
- ✅ Resume parsing works
- ✅ Job tracking works
- ✅ Manual resume editing works

## Comparing to OpenAI

| Feature | Hugging Face | OpenAI |
|---------|-------------|---------|
| Cost | **FREE** | $0.01-0.03 per request |
| Quality | Very good (7B models) | Excellent (GPT-4) |
| Speed | Good (free tier) | Fast |
| Setup | Simple | Requires payment setup |
| Models | Open source | Proprietary |

## Support

For Hugging Face API issues:
- Documentation: https://huggingface.co/docs/api-inference
- Community: https://discuss.huggingface.co/
- Status: https://status.huggingface.co/

For this app's issues:
- Check `SETUP_GUIDE.md`
- Review console logs
- Test with mock optimizer first (no API key)

---

**Ready to optimize your resumes with AI? Get your free API key now!** 🚀



# Railway Deployment Guide

This guide explains how to deploy the MyTaskly MCP Server to Railway using Docker.

## Prerequisites

- Railway account ([railway.app](https://railway.app))
- Git repository connected to Railway
- Environment variables configured in Railway

## Quick Deploy

### Option 1: Deploy from GitHub (Recommended)

1. **Connect Repository to Railway**
   ```bash
   # Push your code to GitHub first
   git add .
   git commit -m "Add Docker configuration for Railway"
   git push origin main
   ```

2. **Create New Project in Railway**
   - Go to [railway.app/new](https://railway.app/new)
   - Click "Deploy from GitHub repo"
   - Select your `MyTaskly-mcp` repository
   - Railway will automatically detect the Dockerfile

3. **Configure Environment Variables**

   In Railway dashboard, go to your service > Variables and add:

   ```env
   # FastAPI Backend
   FASTAPI_BASE_URL=https://your-fastapi-server.railway.app
   FASTAPI_API_KEY=your_api_key_here

   # JWT Configuration (CRITICAL: Must match FastAPI server!)
   JWT_SECRET_KEY=your_jwt_secret_key_here
   JWT_ALGORITHM=HS256
   MCP_AUDIENCE=mytaskly-mcp

   # Server Configuration
   MCP_SERVER_NAME=MyTaskly-MCP
   MCP_SERVER_VERSION=2.0.0
   LOG_LEVEL=INFO

   # Railway automatically provides PORT variable
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - Monitor deployment logs in the Railway dashboard

### Option 2: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Link to your project (if already created)
railway link

# Set environment variables
railway variables set FASTAPI_BASE_URL=https://your-fastapi-server.railway.app
railway variables set JWT_SECRET_KEY=your_jwt_secret_key_here
railway variables set JWT_ALGORITHM=HS256
railway variables set MCP_AUDIENCE=mytaskly-mcp
railway variables set MCP_SERVER_NAME=MyTaskly-MCP
railway variables set MCP_SERVER_VERSION=2.0.0
railway variables set LOG_LEVEL=INFO

# Deploy
railway up
```

## Docker Configuration Files

### Dockerfile

The [Dockerfile](./Dockerfile) includes:
- Python 3.11 slim base image
- Optimized layer caching for faster builds
- Non-root user for security
- Health checks
- Minimal system dependencies

### .dockerignore

The [.dockerignore](./.dockerignore) excludes:
- Virtual environments (`venv/`)
- Python cache files (`__pycache__/`)
- Tests and documentation
- Git files
- IDE configuration

### railway.toml

The [railway.toml](./railway.toml) configures:
- Dockerfile build strategy
- Start command
- Restart policy
- Health checks

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FASTAPI_BASE_URL` | ✅ Yes | FastAPI backend URL | `https://api.mytaskly.com` |
| `FASTAPI_API_KEY` | ✅ Yes | API key for FastAPI | `your_api_key` |
| `JWT_SECRET_KEY` | ✅ Yes | JWT signing key (must match FastAPI) | `your_secret_key` |
| `JWT_ALGORITHM` | ✅ Yes | JWT algorithm | `HS256` |
| `MCP_AUDIENCE` | ✅ Yes | JWT audience claim | `mytaskly-mcp` |
| `MCP_SERVER_NAME` | No | Server name | `MyTaskly-MCP` |
| `MCP_SERVER_VERSION` | No | Version | `2.0.0` |
| `LOG_LEVEL` | No | Logging level | `INFO` |
| `PORT` | Auto | Server port (Railway sets this) | `8000` |

## Security Considerations

### Critical: JWT Secret Key

⚠️ **IMPORTANT**: The `JWT_SECRET_KEY` MUST be identical to your FastAPI server's `SECRET_KEY`.

```bash
# On FastAPI server
SECRET_KEY=my_super_secret_key_12345

# On MCP server (Railway)
JWT_SECRET_KEY=my_super_secret_key_12345  # Must match!
```

If these don't match, JWT token validation will fail!

### Best Practices

1. **Never commit secrets to Git**
   - Use Railway's environment variables
   - Keep `.env` in `.gitignore`

2. **Use strong secret keys**
   ```bash
   # Generate secure key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Enable HTTPS**
   - Railway provides HTTPS by default
   - Never expose HTTP in production

4. **Use short-lived tokens**
   - Recommend 15-30 minute expiration
   - Implement token refresh in your app

## Monitoring & Logs

### View Logs
```bash
# Using Railway CLI
railway logs

# Or in Railway Dashboard
# Go to your service > Logs tab
```

### Health Check

Railway will periodically check your service health. The Dockerfile includes a health check command.

Test health manually:
```bash
curl https://your-app.railway.app/health
```

## Troubleshooting

### Build Failures

**Issue**: Docker build fails with dependency errors

**Solution**:
```bash
# Verify requirements.txt is up to date
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### JWT Token Validation Errors

**Issue**: `Invalid token` or `Token verification failed`

**Solution**:
1. Verify `JWT_SECRET_KEY` matches FastAPI server
2. Check `MCP_AUDIENCE` is correct
3. Ensure token hasn't expired

```bash
# Test token generation on FastAPI server
curl -X POST https://your-fastapi.railway.app/auth/mcp-token \
  -H "Authorization: Bearer YOUR_USER_TOKEN"
```

### Connection to FastAPI Fails

**Issue**: `Connection refused` or timeout errors

**Solution**:
1. Verify `FASTAPI_BASE_URL` is correct
2. Ensure FastAPI server is deployed and running
3. Check Railway service logs for network errors

```bash
# Test FastAPI connectivity
curl https://your-fastapi.railway.app/health
```

### Port Binding Issues

**Issue**: Server fails to start with port errors

**Solution**: Railway automatically sets the `PORT` environment variable. Ensure your `main.py` uses it:

```python
import os
port = int(os.getenv("PORT", 8000))
```

## Scaling & Performance

### Horizontal Scaling

Railway supports horizontal scaling:
- Go to service settings
- Adjust replica count
- MCP server is stateless, safe to scale

### Resource Limits

Monitor resource usage in Railway dashboard:
- CPU usage
- Memory consumption
- Network traffic

Adjust service plan if needed.

## CI/CD Pipeline

Railway automatically deploys when you push to your main branch:

```bash
# Development workflow
git checkout -b feature/new-tool
# Make changes...
git commit -m "feat: add new MCP tool"
git push origin feature/new-tool

# Create PR on GitHub
# After merge to main, Railway auto-deploys
```

## Cost Optimization

1. **Use Starter Plan** for development
2. **Monitor usage** in Railway dashboard
3. **Optimize Docker image size**
   - Use slim base images (already configured)
   - Multi-stage builds if needed
4. **Set sleep policy** for dev environments

## Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Discord**: [discord.gg/railway](https://discord.gg/railway)
- **MyTaskly Issues**: [GitHub Issues](https://github.com/Gabry848/MyTaskly-mcp/issues)

## Next Steps

After deployment:

1. ✅ Test health endpoint
2. ✅ Generate test JWT token
3. ✅ Test MCP tools with token
4. ✅ Update mobile app configuration
5. ✅ Monitor logs for errors

---

**Ready to deploy?** Follow the steps above and your MCP server will be live on Railway! 🚀

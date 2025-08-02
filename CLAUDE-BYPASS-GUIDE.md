# 🚨 Claude Code Bypass Permissions Guide

## ⚠️ SECURITY WARNING
**Bypass permissions mode disables safety checks. Use ONLY in secure, isolated environments!**

## 🚀 Quick Setup Commands

### 1. Run Setup Script
```powershell
# Run the comprehensive setup
powershell -ExecutionPolicy Bypass -File setup-claude-bypass.ps1

# OR run the batch version
.\setup-claude-bypass.bat
```

### 2. Manual Setup (if scripts fail)
```powershell
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Fix PATH permanently
setx PATH "%PATH%;C:\Users\Phill\.local\bin"

# Install project dependencies
npm install

# Build the project
npm run build
```

## 🎯 Claude Code Commands with Bypass

### Basic Bypass Mode
```bash
claude --dangerously-skip-permissions
```

### Verbose Bypass Mode (recommended for debugging)
```bash
claude --dangerously-skip-permissions --verbose
```

### Other Useful Claude Commands
```bash
# Initialize Claude in project
claude /init

# Set up terminal integration
claude /terminal-setup

# Get help
claude /help

# Check status
claude /status
```

## 🛠️ Project Development Commands

### Development
```bash
# Start development server
npm run dev

# Start with auto-reload
npm run dev:watch

# Build project
npm run build

# Start production server
npm start
```

### Code Quality
```bash
# Type check
npm run type-check

# Lint code
npm run lint

# Format code  
npm run format

# Clean build
npm run clean
```

## 🔧 Troubleshooting

### PATH Issues
If Claude commands aren't found:
```powershell
# Check current PATH
echo $env:PATH

# Add manually to current session
$env:PATH += ";C:\Users\Phill\.local\bin"

# Set permanently
setx PATH "%PATH%;C:\Users\Phill\.local\bin"

# Restart terminal after setx command
```

### Permission Issues
```powershell
# Set execution policy for PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run scripts with bypass
powershell -ExecutionPolicy Bypass -File script.ps1
```

### Claude Code Issues
```bash
# Reinstall Claude Code
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code

# Check installation
claude --version

# Update to latest
npm update -g @anthropic-ai/claude-code
```

## 📋 Pre-flight Checklist

Before using bypass mode, verify:

- [ ] ✅ Running in secure, isolated environment
- [ ] ✅ Claude Code installed (`claude --version`)
- [ ] ✅ PATH configured properly
- [ ] ✅ Project dependencies installed (`npm install`)
- [ ] ✅ TypeScript compiles (`npm run build`)
- [ ] ✅ Environment variables configured (`.env` file)
- [ ] ✅ API key properly set in `.env`

## 🎉 Ready to Use!

Once setup is complete:

1. **Start your development server**: `npm run dev`
2. **Open another terminal**
3. **Run Claude with bypass**: `claude --dangerously-skip-permissions --verbose`
4. **Accept the security warning** (only in secure environments!)
5. **Start developing with AI assistance!**

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.anthropic.com/s/claude-code)
- [Claude Code Security Guide](https://docs.anthropic.com/s/claude-code-security)
- Project README: `README.md`
- Health Report: `HEALTH-REPORT.md`

---

**Remember**: Bypass mode is powerful but dangerous. Use responsibly! 🛡️

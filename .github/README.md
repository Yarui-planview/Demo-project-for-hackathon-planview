# GitHub Actions - Automated Code Review

This directory contains GitHub Actions workflows that automatically trigger the review bot from the `let_them_review` repository whenever a PR is submitted.

## Workflows

### 1. `automated-code-review.yml`
- **Trigger**: Pull requests (opened, synchronized, reopened)
- **Purpose**: Main workflow for automated code review
- **Action**: Simply runs `src/bots/review_bot.py` from the `let_them_review` repository

### 2. `pr-review-bot.yml`  
- **Trigger**: Pull requests (skips drafts)
- **Purpose**: Alternative workflow with same functionality
- **Action**: Runs `src/bots/review_bot.py` from the `let_them_review` repository

## Required Secrets

Set up these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

### Required:
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

### Optional (depending on what the review bot needs):
- `OPENAI_API_KEY` - Your OpenAI API key
- `ANTHROPIC_API_KEY` - Your Anthropic API key

## How It Works

1. **PR Created/Updated** → GitHub Actions triggers automatically
2. **Checkout Code** → Downloads your PR code and the review bot repository  
3. **Setup Environment** → Installs Python and review bot dependencies
4. **Run Review Bot** → Executes `src/bots/review_bot.py`
5. **Review Bot Handles Everything** → The bot will:
   - Analyze your code changes
   - Perform security checks
   - Check code quality
   - Handle error cases
   - Post feedback comments on the PR

## Workflow Structure

```yaml
# Simplified workflow steps:
1. Checkout PR code
2. Checkout 'let_them_review' repository  
3. Setup Python 3.9
4. Install dependencies from requirements.txt
5. Run: python src/bots/review_bot.py
```

## Environment Variables Provided

The review bot receives these environment variables:

```bash
GITHUB_TOKEN          # For GitHub API access
GITHUB_REPOSITORY     # Your repository name
GITHUB_PR_NUMBER      # PR number being reviewed
GITHUB_PR_TITLE       # PR title
GITHUB_PR_AUTHOR      # PR author
GITHUB_BASE_REF       # Target branch (usually main)
GITHUB_HEAD_REF       # PR branch
GITHUB_WORKSPACE      # Workspace directory
PR_NUMBER            # PR number
REPO_OWNER           # Repository owner
REPO_NAME            # Repository name
```

## What the Review Bot Does

The `src/bots/review_bot.py` handles all analysis including:
- 🔍 **Code Quality**: Best practices, style, maintainability
- 🔒 **Security**: Vulnerability scanning, injection attacks
- ⚡ **Performance**: Optimization suggestions
- � **Documentation**: Comment quality, README updates
- 🐛 **Error Handling**: Exception handling, edge cases
- 🧪 **Testing**: Test coverage and quality

## Simple Setup

1. **Add Secrets** (if needed by your review bot):
   ```
   Repository Settings → Secrets and variables → Actions
   Add: OPENAI_API_KEY, ANTHROPIC_API_KEY (if required)
   ```

2. **Commit the Workflows** - The `.github/workflows/` files are ready to use

3. **Create a PR** - The review bot will automatically run!

## Troubleshooting

- **Bot not running**: Check if `let_them_review` repository is accessible
- **Permission issues**: Verify GITHUB_TOKEN has required permissions  
- **Missing dependencies**: Review bot should include `requirements.txt`
- **API errors**: Check if API key secrets are configured correctly

The review bot at `src/bots/review_bot.py` is responsible for all the analysis and feedback - these workflows simply trigger it with the right environment and context.

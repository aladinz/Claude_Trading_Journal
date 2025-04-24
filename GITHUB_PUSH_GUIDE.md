# GitHub Push Guide

Follow these steps to push your code to the GitHub repository:

## Option 1: Using HTTPS

1. Navigate to your project directory:
   ```
   cd /mnt/c/users/aladi/claudeprojects/trading_journal
   ```

2. Ensure your git user is configured:
   ```
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

3. Push to GitHub (you'll be prompted for your GitHub username and password/token):
   ```
   git push -u origin main
   ```

   Note: GitHub no longer accepts passwords for HTTPS Git operations. You'll need to use a personal access token instead.

## Option 2: Using SSH

1. Generate an SSH key if you don't have one:
   ```
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. Add your SSH key to the ssh-agent:
   ```
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

3. Add your public SSH key to your GitHub account:
   - Copy the SSH key: `cat ~/.ssh/id_ed25519.pub`
   - Go to GitHub > Settings > SSH and GPG keys > New SSH key
   - Paste your key and save

4. Change your remote URL to use SSH:
   ```
   git remote set-url origin git@github.com:aladinz/Claude_Trading_Journal.git
   ```

5. Push to GitHub:
   ```
   git push -u origin main
   ```

## Option 3: Using GitHub CLI

1. Install GitHub CLI if not already installed:
   ```
   # For Ubuntu/Debian
   sudo apt install gh
   
   # For Windows
   winget install --id GitHub.cli
   ```

2. Authenticate with GitHub:
   ```
   gh auth login
   ```

3. Push using GitHub CLI:
   ```
   gh repo create aladinz/Claude_Trading_Journal --source=. --public --push
   ```

## After Successfully Pushing to GitHub

Once your code is on GitHub, you can deploy it to Vercel:

1. Sign up/in at [vercel.com](https://vercel.com)
2. Connect your GitHub account to Vercel
3. Import your repository
4. Configure the following settings:
   - Framework Preset: Other
   - Build Command: ./build_steps.sh
   - Output Directory: None needed
   - Install Command: pip install -r requirements-vercel.txt
5. Add environment variables:
   - `SECRET_KEY`: A secure random string
   - `DATABASE_URL`: (Optional) For a persistent database
6. Deploy!
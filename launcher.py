#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def check_docker():
    """Check if Docker is installed and running."""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Docker is not installed or not in PATH. Please install Docker first.")
        exit(1)

    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Docker daemon is not running. Please start Docker first.")
        exit(1)

def load_api_key():
    """Load OpenAI API key from .env file."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OpenAI API key not found in .env file.")
        print("Please add your API key to .env file:")
        print('OPENAI_API_KEY=your_key_here')
        exit(1)
    return api_key

def pull_image():
    """Pull the PPTAgent Docker image."""
    print("Pulling PPTAgent Docker image...")
    try:
        subprocess.run(["docker", "pull", "forceless/pptagent"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to pull Docker image. Please check your internet connection.")
        exit(1)

def run_container(api_key):
    """Run the PPTAgent Docker container."""
    print("Starting PPTAgent container...")
    try:
        # Stop and remove existing container if it exists
        subprocess.run(["docker", "rm", "-f", "pptagent"], check=False, capture_output=True)
        
        # Run new container
        cmd = [
            "docker", "run",
            "-dt",
            "--gpus", "all",
            "--ipc=host",
            "--name", "pptagent",
            "-e", f"OPENAI_API_KEY={api_key}",
            "-p", "9297:9297",
            "-p", "8088:8088",
            "-v", f"{str(Path.home())}:/root",
            "forceless/pptagent"
        ]
        subprocess.run(cmd, check=True)
        print("\nPPTAgent container started successfully!")
        print("- Backend API available at: http://localhost:9297")
        print("- Frontend UI available at: http://localhost:8088")
        
        # Show container logs
        print("\nContainer logs:")
        subprocess.run(["docker", "logs", "-f", "pptagent"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to run container: {e}")
        exit(1)

def main():
    """Main function to launch PPTAgent."""
    print("Starting PPTAgent...\n")
    
    # Check requirements
    check_docker()
    api_key = load_api_key()
    
    # Pull and run container
    pull_image()
    run_container(api_key)

if __name__ == "__main__":
    main()

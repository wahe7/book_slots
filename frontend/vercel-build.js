// This script is used by Vercel to build the project
const { execSync } = require('child_process');

function runCommand(command) {
  try {
    console.log(`Running: ${command}`);
    const output = execSync(command, { stdio: 'inherit' });
    return true;
  } catch (error) {
    console.error(`Error executing command: ${command}`);
    console.error(error.message);
    process.exit(1);
  }
}

console.log('Starting Vercel build...');

// Install dependencies
console.log('Installing dependencies...');
runCommand('npm install --prefer-offline --no-audit --progress=false');

// Build the project
console.log('Building project...');
runCommand('npm run build');

console.log('Build completed successfully!');

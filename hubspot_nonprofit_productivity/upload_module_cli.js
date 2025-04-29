#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

/**
 * Main entry point that uploads a module to HubSpot using the HubSpot CLI.
 */
function main() {
  // Determine which module directory to upload.
  // Default directory is "modules/quantity-selector", but you can pass a different path as the first CLI argument.
  const args = process.argv.slice(2);
  const srcFolder = args[0] ? path.resolve(args[0]) : path.resolve(__dirname, 'modules', 'quantity-selector');
  // Destination folder in HubSpot; defaults to the basename of the source folder.
  const destFolder = args[1] ? args[1] : path.basename(srcFolder);

  if (!fs.existsSync(srcFolder)) {
    console.error(`Module directory ${srcFolder} does not exist.`);
    process.exit(1);
  }
  
  // Construct the relative source path from the current working directory
  const relativeSrc = path.relative(process.cwd(), srcFolder);

  // Construct the hs upload command following HubSpot documentation
  const cmd = `hs upload "${relativeSrc}" "${destFolder}"`;
  console.log(`Executing command: ${cmd}`);
  
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error during hub upload: ${error.message}`);
      process.exit(1);
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
    }
    console.log(`Upload successful. Output:\n${stdout}`);
  });
}

if (require.main === module) {
  main();
} 
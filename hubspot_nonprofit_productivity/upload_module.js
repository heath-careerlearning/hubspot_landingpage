#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const axios = require('axios');
const yaml = require('js-yaml');
const archiver = require('archiver');
const FormData = require('form-data');

/**
 * Main entry point that uploads a module to HubSpot.
 */
async function main() {
  try {
    // Determine which module directory to upload.
    // Default directory is "modules/quantity-selector", but you can pass a different path as the first CLI argument.
    const args = process.argv.slice(2);
    const moduleDir = args[0]
      ? path.resolve(args[0])
      : path.resolve(__dirname, 'modules', 'quantity-selector');

    if (!fs.existsSync(moduleDir)) {
      throw new Error(`Module directory ${moduleDir} does not exist.`);
    }

    // Load HubSpot configuration from hubspot.config.yml.
    const configFilePath = path.resolve(__dirname, 'hubspot.config.yml');
    if (!fs.existsSync(configFilePath)) {
      throw new Error(`Configuration file ${configFilePath} not found.`);
    }
    const configContent = fs.readFileSync(configFilePath, 'utf8');
    const config = yaml.load(configContent);

    // Get the default portal configuration.
    const defaultPortalName = config.defaultPortal;
    const portalConfig = config.portals.find(p => p.name === defaultPortalName);
    if (!portalConfig) {
      throw new Error(`Default portal '${defaultPortalName}' not found in configuration.`);
    }
    const portalId = portalConfig.portalId;
    const accessToken = portalConfig.auth.tokenInfo.accessToken;
    const uploadMode = config.options && config.options.uploadMode ? config.options.uploadMode : 'draft';

    console.log(`Uploading module from directory: ${moduleDir}`);
    console.log(`Using portal ID: ${portalId}`);

    // Create a zip archive of the module directory in a temporary file.
    const zipFilePath = path.join(os.tmpdir(), `module_${Date.now()}.zip`);
    await createZip(moduleDir, zipFilePath);
    console.log(`Created zip archive at: ${zipFilePath}`);

    // Upload the module zip file to HubSpot.
    const response = await uploadModule(zipFilePath, accessToken, portalId, uploadMode);
    console.log('Upload successful. Response data:');
    console.log(response.data);
  } catch (err) {
    console.error('Error during module upload:', err.message);
    process.exit(1);
  }
}

/**
 * Creates a zip archive of the given source directory.
 * @param {string} srcDir - The directory to be zipped.
 * @param {string} outPath - The output zip file path.
 */
function createZip(srcDir, outPath) {
  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(outPath);
    const archive = archiver('zip', { zlib: { level: 9 } });

    output.on('close', () => resolve());
    archive.on('error', err => reject(err));

    archive.pipe(output);
    // Include the contents of the module directory directly (skip the root folder).
    archive.directory(srcDir, false);
    archive.finalize();
  });
}

/**
 * Uploads the module zip file to HubSpot via the API.
 * @param {string} zipFile - The path to the zip file.
 * @param {string} accessToken - The HubSpot access token.
 * @param {number|string} portalId - The HubSpot portal ID.
 * @param {string} uploadMode - The upload mode (e.g., 'draft').
 * @returns {Promise} Axios response promise.
 */
async function uploadModule(zipFile, accessToken, portalId, uploadMode) {
  // Prepare the form data for the file upload.
  const form = new FormData();
  form.append('file', fs.createReadStream(zipFile));

  // The endpoint URL is a placeholder—adjust it based on the relevant HubSpot API documentation.
  const uploadUrl = process.env.HUBSPOT_MODULE_UPLOAD_URL;
  if (!uploadUrl) {
    throw new Error("HUBSPOT_MODULE_UPLOAD_URL environment variable not set. Please set it to the correct endpoint for module upload as per HubSpot documentation.");
  }
  const endpoint = `${uploadUrl}?portalId=${portalId}&uploadMode=${uploadMode}`;
  console.log(`Uploading module to endpoint: ${endpoint}`);

  try {
    const response = await axios.post(endpoint, form, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        ...form.getHeaders()
      },
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });
    return response;
  } catch (err) {
    throw new Error(`Failed to upload module: ${err.response ? JSON.stringify(err.response.data) : err.message}`);
  }
}

if (require.main === module) {
  main();
}
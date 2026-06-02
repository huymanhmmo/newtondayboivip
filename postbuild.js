import fs from 'fs';
import path from 'path';

console.log('[postbuild] Starting postbuild processing...');
console.log('[postbuild] Current working directory:', process.cwd());

const filesToProcess = [
  'dist/client/wrangler.json',
  'dist/server/wrangler.json',
  'dist/server/.prerender/wrangler.json'
];

filesToProcess.forEach(filePath => {
  const fullPath = path.resolve(filePath);
  console.log(`[postbuild] Checking file: ${filePath} -> Resolved to: ${fullPath}`);
  if (fs.existsSync(fullPath)) {
    console.log(`[postbuild] File exists: ${filePath}`);
    try {
      const content = fs.readFileSync(fullPath, 'utf8');
      const data = JSON.parse(content);
      
      let modified = false;
      if (data.kv_namespaces) {
        console.log(`[postbuild] Original kv_namespaces in ${filePath}:`, JSON.stringify(data.kv_namespaces));
        const originalLength = data.kv_namespaces.length;
        data.kv_namespaces = data.kv_namespaces.filter(kv => kv.binding !== 'SESSION');
        if (data.kv_namespaces.length !== originalLength) {
          modified = true;
          console.log(`[postbuild] Removed SESSION from kv_namespaces in ${filePath}`);
        }
      }
      if (data.previews && data.previews.kv_namespaces) {
        console.log(`[postbuild] Original previews.kv_namespaces in ${filePath}:`, JSON.stringify(data.previews.kv_namespaces));
        const originalLength = data.previews.kv_namespaces.length;
        data.previews.kv_namespaces = data.previews.kv_namespaces.filter(kv => kv.binding !== 'SESSION');
        if (data.previews.kv_namespaces.length !== originalLength) {
          modified = true;
          console.log(`[postbuild] Removed SESSION from previews.kv_namespaces in ${filePath}`);
        }
      }
      
      if (modified) {
        fs.writeFileSync(fullPath, JSON.stringify(data), 'utf8');
        console.log(`[postbuild] Successfully wrote updated config to ${filePath}`);
      } else {
        console.log(`[postbuild] No modifications needed for ${filePath}`);
      }
    } catch (err) {
      console.error(`[postbuild] Error processing ${filePath}:`, err);
    }
  } else {
    console.log(`[postbuild] File does not exist: ${filePath}`);
  }
});

import fs from 'fs';
import path from 'path';

const filesToProcess = [
  'dist/client/wrangler.json',
  'dist/server/.prerender/wrangler.json'
];

filesToProcess.forEach(filePath => {
  const fullPath = path.resolve(filePath);
  if (fs.existsSync(fullPath)) {
    try {
      const content = fs.readFileSync(fullPath, 'utf8');
      const data = JSON.parse(content);
      
      let modified = false;
      if (data.kv_namespaces) {
        data.kv_namespaces = data.kv_namespaces.filter(kv => kv.binding !== 'SESSION');
        modified = true;
      }
      if (data.previews && data.previews.kv_namespaces) {
        data.previews.kv_namespaces = data.previews.kv_namespaces.filter(kv => kv.binding !== 'SESSION');
        modified = true;
      }
      
      if (modified) {
        fs.writeFileSync(fullPath, JSON.stringify(data), 'utf8');
        console.log(`[postbuild] Successfully removed SESSION KV namespace from ${filePath}`);
      }
    } catch (err) {
      console.error(`[postbuild] Error processing ${filePath}:`, err);
    }
  }
});

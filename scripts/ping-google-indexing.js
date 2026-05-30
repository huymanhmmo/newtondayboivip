import fs from 'fs';
import path from 'path';
import { JWT } from 'google-auth-library';

// Helper to parse frontmatter from markdown file
function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return {};
  
  const frontmatterText = match[1];
  const data = {};
  
  frontmatterText.split('\n').forEach(line => {
    const colonIdx = line.indexOf(':');
    if (colonIdx !== -1) {
      const key = line.slice(0, colonIdx).trim();
      let value = line.slice(colonIdx + 1).trim();
      // Remove surrounding quotes if any
      if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
      if (value.startsWith("'") && value.endsWith("'")) value = value.slice(1, -1);
      data[key] = value;
    }
  });
  
  return data;
}

async function main() {
  const credentialsJson = process.env.GOOGLE_INDEXING_CREDENTIALS;
  if (!credentialsJson) {
    console.log("⚠️  GOOGLE_INDEXING_CREDENTIALS environment variable is not defined. Skipping Google Indexing API ping.");
    process.exit(0);
  }

  let credentials;
  try {
    credentials = JSON.parse(credentialsJson);
  } catch (e) {
    console.error("❌ Failed to parse GOOGLE_INDEXING_CREDENTIALS as JSON:", e.message);
    process.exit(1);
  }

  const domain = "https://newton.dayboi.vip";
  const urlsToPing = [
    `${domain}/`,
    `${domain}/cam-nang`
  ];

  // Read all blog posts to find recent ones
  const blogDir = path.join(process.cwd(), 'src/content/blog');
  if (fs.existsSync(blogDir)) {
    const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.md'));
    const today = new Date();
    
    files.forEach(file => {
      const filePath = path.join(blogDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const meta = parseFrontmatter(content);
      
      if (meta.pubDate) {
        // Handle pubDate which might be like "2026-05-31 08:30:00 +07:00"
        const dateClean = meta.pubDate.split()[0].replace('"', '').replace("'", "");
        const pubDate = new Date(dateClean);
        
        // Check if pubDate is within the last 7 days (or in the future, just in case)
        const diffTime = today.getTime() - pubDate.getTime();
        const diffDays = diffTime / (1000 * 60 * 60 * 24);
        
        if (diffDays <= 7) {
          const slug = file.replace('.md', '');
          urlsToPing.push(`${domain}/cam-nang/${slug}`);
        }
      }
    });
  }

  console.log(`🚀 Found ${urlsToPing.length} URL(s) to submit to Google Indexing API:`);
  urlsToPing.forEach(url => console.log(` - ${url}`));

  // Initialize Google Auth Client
  const client = new JWT({
    email: credentials.client_email,
    key: credentials.private_key,
    scopes: ['https://www.googleapis.com/auth/indexing'],
  });

  try {
    console.log("🔑 Authenticating with Google APIs...");
    await client.authorize();
    console.log("🔒 Authentication successful. Sending indexing requests...");
    
    for (const url of urlsToPing) {
      try {
        const response = await client.request({
          url: 'https://indexing.googleapis.com/v3/urlNotifications:publish',
          method: 'POST',
          data: {
            url: url,
            type: 'URL_UPDATED',
          },
        });
        console.log(`✅ Indexing request sent for: ${url} (Response code: ${response.status})`);
      } catch (err) {
        console.error(`❌ Failed to send indexing request for: ${url}`, err.message);
      }
    }
  } catch (err) {
    console.error("❌ Google Indexing API Authentication failed:", err.message);
    process.exit(1);
  }
}

main();

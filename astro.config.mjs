// @ts-check
import { defineConfig, sessionDrivers } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

// https://astro.build/config
export default defineConfig({
  adapter: cloudflare(),
  build: {
    assets: 'assets'
  },
  session: {
    driver: sessionDrivers.memory()
  }
});
